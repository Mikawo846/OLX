import requests
import time
import re
from typing import List, Dict, Optional
import config
import logging

logger = logging.getLogger(__name__)

SEARCH_KEYWORDS = {
    'camera': 'фотоаппарат камера Canon Nikon Sony',
    'phone': 'телефон мобильный',
    'smartphone': 'смартфон iPhone Samsung Xiaomi',
    'computer': 'компьютер ноутбук ПК',
    'tablet': 'планшет iPad tablet',
    'gaming': 'PlayStation Xbox Nintendo приставка'
}

class OLXScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT,
            'Accept': 'application/json',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.api_base = 'https://www.olx.kz/api/v1/offers/'
    
    def fetch_ads(self, category_url: str, category_id: str, max_pages: int = 10) -> List[Dict]:
        all_ads = []
        
        search_query = SEARCH_KEYWORDS.get(category_id, 'электроника')
        
        limit = 40
        for page in range(max_pages):
            try:
                offset = page * limit
                api_url = f"{self.api_base}?offset={offset}&limit={limit}&query={search_query}"
                
                logger.info(f"Searching API: '{search_query}' offset={offset}")
                
                response = self.session.get(
                    api_url,
                    timeout=config.REQUEST_TIMEOUT
                )
                
                if response.status_code != 200:
                    logger.error(f"HTTP {response.status_code} for API request")
                    break
                
                data = response.json()
                ads_data = data.get('data', [])
                
                if not ads_data:
                    logger.info(f"No more ads found at offset {offset}")
                    break
                
                ads = self._parse_api_response(ads_data, category_id)
                all_ads.extend(ads)
                
                logger.info(f"Found {len(ads)} ads at offset {offset}")
                
            except Exception as e:
                logger.error(f"Error fetching from API: {e}")
                break
        
        return all_ads
    
    def _parse_api_response(self, ads_data: List[Dict], category_id: str) -> List[Dict]:
        ads = []
        
        for ad_raw in ads_data:
            try:
                ad_data = self._extract_ad_from_api(ad_raw, category_id)
                if ad_data:
                    ads.append(ad_data)
            except Exception as e:
                logger.debug(f"Error parsing ad from API: {e}")
                continue
        
        return ads
    
    def _extract_ad_from_api(self, ad_raw: Dict, category_id: str) -> Optional[Dict]:
        try:
            ad_id = str(ad_raw.get('id', ''))
            if not ad_id:
                return None
            
            title = ad_raw.get('title', '').strip()
            url = ad_raw.get('url', '')
            
            params = ad_raw.get('params', [])
            price = 0.0
            for param in params:
                if param.get('key') == 'price':
                    price_value = param.get('value', {})
                    if isinstance(price_value, dict):
                        price = float(price_value.get('value', 0))
                    else:
                        price = self._extract_price(str(price_value))
                    break
            
            location_data = ad_raw.get('location', {})
            city = location_data.get('city', {}).get('name', '')
            region = location_data.get('region', {}).get('name', '')
            location = f"{city}, {region}" if city and region else city or region
            
            photos = ad_raw.get('photos', [])
            image_url = photos[0].get('link') if photos else ''
            
            if not title or price == 0:
                return None
            
            return {
                'id': ad_id,
                'title': title,
                'price': price,
                'currency': 'KZT',
                'url': url,
                'location': location,
                'image_url': image_url,
                'category': category_id,
                'description': ad_raw.get('description', '')
            }
            
        except Exception as e:
            logger.debug(f"Error extracting ad from API data: {e}")
            return None
    
    def _extract_price(self, price_text: str) -> float:
        try:
            price_text = price_text.replace(' ', '').replace('\xa0', '')
            
            numbers = re.findall(r'\d+', price_text)
            if numbers:
                price_str = ''.join(numbers)
                return float(price_str)
            
            return 0.0
        except:
            return 0.0
    
