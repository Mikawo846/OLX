import logging
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import config
from parser_engine import ParserEngine

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('olx_parser.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_category_wrapper(category_config):
    engine = ParserEngine()
    try:
        return engine.process_category(category_config)
    finally:
        engine.close()

def run_parallel_scraping():
    logger.info("=" * 80)
    logger.info(f"Starting OLX scraping session at {datetime.now()}")
    logger.info("=" * 80)
    
    total_stats = {
        'total_ads': 0,
        'total_new': 0,
        'total_deals': 0,
        'categories_processed': 0
    }
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_category = {
            executor.submit(process_category_wrapper, cat): cat 
            for cat in config.OLX_CATEGORIES
        }
        
        for future in as_completed(future_to_category):
            category = future_to_category[future]
            try:
                stats = future.result()
                total_stats['total_ads'] += stats['ads_found']
                total_stats['total_new'] += stats['new_ads']
                total_stats['total_deals'] += stats['good_deals']
                total_stats['categories_processed'] += 1
                
                logger.info(f"Category {category['name']} completed: "
                          f"{stats['ads_found']} ads, "
                          f"{stats['new_ads']} new, "
                          f"{stats['good_deals']} deals")
            except Exception as e:
                logger.error(f"Category {category['name']} failed: {e}")
    
    logger.info("=" * 80)
    logger.info(f"Session completed at {datetime.now()}")
    logger.info(f"Summary: {total_stats['categories_processed']} categories, "
              f"{total_stats['total_ads']} total ads, "
              f"{total_stats['total_new']} new ads, "
              f"{total_stats['total_deals']} good deals found")
    logger.info("=" * 80)
    
    return total_stats

def run_continuous():
    logger.info("Starting continuous OLX parser")
    logger.info(f"Discount threshold: {config.DISCOUNT_THRESHOLD * 100}%")
    logger.info(f"Categories: {len(config.OLX_CATEGORIES)}")
    logger.info("Running at MAXIMUM SPEED - no delays!")
    
    iteration = 0
    
    while True:
        try:
            iteration += 1
            logger.info(f"\n{'='*80}\nIteration #{iteration}\n{'='*80}")
            
            stats = run_parallel_scraping()
            
        except KeyboardInterrupt:
            logger.info("\nStopping parser (Ctrl+C pressed)")
            break
        except Exception as e:
            logger.error(f"Critical error in main loop: {e}", exc_info=True)
            logger.info("Waiting 10 seconds before retry...")
            time.sleep(10)

def run_single():
    logger.info("Running single scraping session")
    stats = run_parallel_scraping()
    logger.info("Single session completed")
    return stats

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        run_single()
    else:
        run_continuous()
