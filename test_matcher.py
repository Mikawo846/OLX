import logging
from model_matcher import ModelMatcher
from database import SessionLocal, ReferenceModel

logging.basicConfig(level=logging.INFO)

def test_matcher():
    print("Testing Model Matcher...")
    print("=" * 80)
    
    db = SessionLocal()
    model_count = db.query(ReferenceModel).count()
    print(f"\nModels in database: {model_count}")
    
    if model_count == 0:
        print("\n⚠️  No models found in database!")
        print("Run: python import_base.py")
        return
    
    print("\nSample models:")
    samples = db.query(ReferenceModel).limit(5).all()
    for s in samples:
        print(f"  - {s.brand} {s.model_name} ({s.base_price} ₸)")
    
    print("\n" + "=" * 80)
    print("Testing matching algorithm...")
    print("=" * 80 + "\n")
    
    matcher = ModelMatcher()
    
    test_cases = [
        ("Canon 80D body в отличном состоянии", "", "camera"),
        ("Nikon D5300 kit 18-55", "", "camera"),
        ("Продам Canon 5D Mark III", "", "camera"),
        ("Фотоаппарат Sony A7", "", "camera"),
        ("Canon 700D + объектив", "", "camera"),
        ("Битый Canon 80D", "", "camera"),
    ]
    
    for title, desc, category in test_cases:
        print(f"Testing: '{title}'")
        result = matcher.match_ad_to_model(title, desc, category)
        
        if result:
            model, score = result
            print(f"  ✓ Matched: {model.brand} {model.model_name}")
            print(f"    Score: {score:.1f}")
            print(f"    Base price: {model.base_price} ₸")
        else:
            print(f"  ✗ No match found")
        print()
    
    matcher.close()
    db.close()

if __name__ == '__main__':
    test_matcher()
