from typing import Optional, Dict
import logging
import config
from database import ReferenceModel

logger = logging.getLogger(__name__)

class PriceChecker:
    def __init__(self, discount_threshold: float = None):
        self.discount_threshold = discount_threshold or config.DISCOUNT_THRESHOLD
    
    def is_good_deal(self, ad_price: float, model: ReferenceModel) -> Optional[Dict]:
        if ad_price < config.MIN_REAL_PRICE:
            logger.debug(f"Price {ad_price} is below minimum real price threshold")
            return None
        
        if ad_price <= 0 or model.base_price <= 0:
            logger.debug(f"Invalid prices: ad={ad_price}, base={model.base_price}")
            return None
        
        threshold_price = model.base_price * (1 - self.discount_threshold)
        
        if ad_price <= threshold_price:
            discount_percent = ((model.base_price - ad_price) / model.base_price) * 100
            
            deal_info = {
                'is_good_deal': True,
                'ad_price': ad_price,
                'base_price': model.base_price,
                'threshold_price': threshold_price,
                'discount_percent': discount_percent,
                'savings': model.base_price - ad_price
            }
            
            logger.info(f"Good deal found! Price {ad_price} vs base {model.base_price} ({discount_percent:.1f}% off)")
            return deal_info
        
        return None
    
    def calculate_discount(self, ad_price: float, base_price: float) -> float:
        if base_price <= 0:
            return 0.0
        return ((base_price - ad_price) / base_price) * 100
