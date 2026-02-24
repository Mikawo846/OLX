import logging
from typing import List, Dict
from datetime import datetime
from database import SessionLocal, ProcessedAd, ScraperLog, ReferenceModel
from olx_scraper import OLXScraper
from model_matcher import ModelMatcher
from price_checker import PriceChecker
from telegram_notifier import TelegramNotifier
import config

logger = logging.getLogger(__name__)

class ParserEngine:
    def __init__(self):
        self.scraper = OLXScraper()
        self.matcher = ModelMatcher()
        self.price_checker = PriceChecker()
        self.notifier = TelegramNotifier()
        self.db = SessionLocal()
    
    def process_category(self, category_config: Dict) -> Dict:
        category_name = category_config['name']
        category_url = category_config['url']
        category_id = category_config['category_id']
        
        logger.info(f"Processing category: {category_name}")
        
        stats = {
            'category': category_id,
            'ads_found': 0,
            'new_ads': 0,
            'good_deals': 0,
            'errors': []
        }
        
        try:
            ads = self.scraper.fetch_ads(category_url, category_id, max_pages=3)
            stats['ads_found'] = len(ads)
            
            logger.info(f"Found {len(ads)} ads in {category_name}")
            
            for ad in ads:
                try:
                    self._process_single_ad(ad, stats)
                except Exception as e:
                    error_msg = f"Error processing ad {ad.get('id')}: {e}"
                    logger.error(error_msg)
                    stats['errors'].append(error_msg)
            
            self._log_scraper_run(stats)
            
        except Exception as e:
            error_msg = f"Error processing category {category_name}: {e}"
            logger.error(error_msg)
            stats['errors'].append(error_msg)
            self._log_scraper_run(stats, status='error')
        
        return stats
    
    def _process_single_ad(self, ad: Dict, stats: Dict):
        ad_id = ad['id']
        
        existing = self.db.query(ProcessedAd).filter(ProcessedAd.olx_ad_id == ad_id).first()
        if existing:
            logger.debug(f"Ad {ad_id} already processed, skipping")
            return
        
        stats['new_ads'] += 1
        
        match_result = self.matcher.match_ad_to_model(
            ad['title'],
            ad.get('description', ''),
            ad['category']
        )
        
        if not match_result:
            self._save_unmatched_ad(ad)
            return
        
        model, match_score = match_result
        
        deal_info = self.price_checker.is_good_deal(ad['price'], model)
        
        if deal_info:
            stats['good_deals'] += 1
            
            notification_sent = self.notifier.send_notification_sync(ad, model, deal_info)
            
            self._save_processed_ad(ad, model, deal_info, notification_sent)
            
            logger.info(f"✓ Good deal saved and notified: {ad['title']}")
        else:
            self._save_processed_ad(ad, model, None, False)
    
    def _save_processed_ad(self, ad: Dict, model: ReferenceModel, deal_info: Dict = None, notification_sent: bool = False):
        processed_ad = ProcessedAd(
            olx_ad_id=ad['id'],
            category=ad['category'],
            title=ad['title'],
            price=ad['price'],
            url=ad['url'],
            matched_model_id=model.id,
            discount_percent=deal_info['discount_percent'] if deal_info else 0,
            notification_sent=notification_sent,
            notification_sent_at=datetime.utcnow() if notification_sent else None
        )
        
        self.db.add(processed_ad)
        self.db.commit()
    
    def _save_unmatched_ad(self, ad: Dict):
        processed_ad = ProcessedAd(
            olx_ad_id=ad['id'],
            category=ad['category'],
            title=ad['title'],
            price=ad['price'],
            url=ad['url'],
            matched_model_id=None,
            discount_percent=0,
            notification_sent=False
        )
        
        self.db.add(processed_ad)
        self.db.commit()
        
        logger.debug(f"Saved unmatched ad: {ad['title']}")
    
    def _log_scraper_run(self, stats: Dict, status: str = 'success'):
        log_entry = ScraperLog(
            category=stats['category'],
            ads_found=stats['ads_found'],
            new_ads=stats['new_ads'],
            good_deals=stats['good_deals'],
            errors='\n'.join(stats['errors']) if stats['errors'] else None,
            status=status
        )
        
        self.db.add(log_entry)
        self.db.commit()
    
    def close(self):
        self.matcher.close()
        self.db.close()
