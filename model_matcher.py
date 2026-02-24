from typing import Optional, List, Tuple
from fuzzywuzzy import fuzz
import re
import logging
from database import ReferenceModel, SessionLocal
import config

logger = logging.getLogger(__name__)

class ModelMatcher:
    def __init__(self):
        self.db = SessionLocal()
        self.models_cache = {}
        self._load_models()
    
    def _load_models(self):
        models = self.db.query(ReferenceModel).filter(ReferenceModel.active == True).all()
        
        for category in ['camera', 'phone', 'smartphone', 'computer', 'tablet', 'gaming']:
            self.models_cache[category] = []
        
        for model in models:
            category = model.category or 'camera'
            if category not in self.models_cache:
                self.models_cache[category] = []
            self.models_cache[category].append(model)
        
        total = sum(len(v) for v in self.models_cache.values())
        logger.info(f"Loaded {total} active models into cache")
    
    def reload_models(self):
        self._load_models()
    
    def match_ad_to_model(self, ad_title: str, ad_description: str, category: str) -> Optional[Tuple[ReferenceModel, float]]:
        ad_text = f"{ad_title} {ad_description}".lower()
        
        for ignore_word in config.IGNORE_WORDS:
            if ignore_word.strip() and ignore_word.strip().lower() in ad_text:
                logger.debug(f"Ad contains ignore word '{ignore_word}': {ad_title}")
                return None
        
        models_to_check = self.models_cache.get(category, [])
        
        if not models_to_check and category in ['phone', 'smartphone']:
            alt_category = 'smartphone' if category == 'phone' else 'phone'
            models_to_check.extend(self.models_cache.get(alt_category, []))
        
        if not models_to_check:
            logger.debug(f"No models found for category '{category}'")
            return None
        
        best_match = None
        best_score = 0
        
        for model in models_to_check:
            brand_lower = model.brand.lower()
            
            if brand_lower not in ad_text:
                continue
            
            score = self._calculate_match_score(ad_text, model)
            
            if score > best_score:
                best_score = score
                best_match = model
        
        if best_score >= 80:
            logger.info(f"Matched '{ad_title}' to {best_match.brand} {best_match.model_name} (score: {best_score})")
            return best_match, best_score
        
        logger.debug(f"No good match for '{ad_title}' (best score: {best_score})")
        return None
    
    def _calculate_match_score(self, ad_text: str, model: ReferenceModel) -> float:
        scores = []
        
        full_name = f"{model.brand} {model.model_name}".lower()
        score1 = fuzz.partial_ratio(full_name, ad_text)
        scores.append(score1)
        
        if model.search_keywords:
            keywords = model.search_keywords.split('|')
            for keyword in keywords:
                keyword = keyword.strip().lower()
                if keyword in ad_text:
                    scores.append(100)
                else:
                    score = fuzz.partial_ratio(keyword, ad_text)
                    scores.append(score)
        
        brand_lower = model.brand.lower()
        model_lower = model.model_name.lower()
        
        if brand_lower in ad_text and model_lower in ad_text:
            scores.append(95)
        
        model_tokens = re.findall(r'\w+', model_lower)
        matches = sum(1 for token in model_tokens if token in ad_text)
        if model_tokens:
            token_score = (matches / len(model_tokens)) * 100
            scores.append(token_score)
        
        return max(scores) if scores else 0
    
    def close(self):
        self.db.close()
