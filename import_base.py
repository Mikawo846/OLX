import pandas as pd
from database import SessionLocal, ReferenceModel, init_db
import re

def extract_brand_model(full_name):
    full_name = full_name.strip()
    
    brands = ['Canon', 'Nikon', 'Sony', 'Fujifilm', 'Panasonic', 'Olympus', 
              'Pentax', 'Leica', 'Samsung', 'Apple', 'Xiaomi', 'Huawei',
              'Oppo', 'Vivo', 'Realme', 'OnePlus', 'Lenovo', 'Asus', 
              'HP', 'Dell', 'Acer', 'MSI', 'GoPro', 'DJI']
    
    brand = None
    for b in brands:
        if full_name.startswith(b):
            brand = b
            model = full_name[len(b):].strip()
            break
    
    if not brand:
        parts = full_name.split(' ', 1)
        brand = parts[0]
        model = parts[1] if len(parts) > 1 else full_name
    
    return brand, model

def generate_search_keywords(brand, model_name):
    keywords = []
    
    full_name = f"{brand} {model_name}".lower()
    keywords.append(full_name)
    
    keywords.append(model_name.lower())
    
    no_space = model_name.replace(' ', '').lower()
    if no_space != model_name.lower():
        keywords.append(no_space)
    
    with_dash = model_name.replace(' ', '-').lower()
    if with_dash != model_name.lower():
        keywords.append(with_dash)
    
    return '|'.join(set(keywords))

def import_base_xlsx(file_path='base.xlsx'):
    init_db()
    
    df = pd.read_excel(file_path, header=None)
    df.columns = ['brand_model', 'separator', 'price']
    
    db = SessionLocal()
    
    try:
        existing_count = db.query(ReferenceModel).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} models. Skipping import.")
            print("To re-import, delete olx_parser.db and run again.")
            return
        
        imported = 0
        for idx, row in df.iterrows():
            brand_model = str(row['brand_model']).strip()
            price_str = str(row['price']).replace(' ', '').replace('\xa0', '')
            
            try:
                price = float(price_str)
            except (ValueError, TypeError):
                continue
            
            if pd.isna(brand_model) or price <= 0:
                continue
            
            brand, model_name = extract_brand_model(brand_model)
            search_keywords = generate_search_keywords(brand, model_name)
            
            ref_model = ReferenceModel(
                brand=brand,
                model_name=model_name,
                base_price=price,
                category='camera',
                search_keywords=search_keywords,
                active=True
            )
            
            db.add(ref_model)
            imported += 1
            
            if imported % 50 == 0:
                db.commit()
                print(f"Imported {imported} models...")
        
        db.commit()
        print(f"\n✓ Successfully imported {imported} models from {file_path}")
        
        print("\nSample imported data:")
        samples = db.query(ReferenceModel).limit(5).all()
        for s in samples:
            print(f"  {s.brand} {s.model_name} - {s.base_price} тг")
        
    except Exception as e:
        db.rollback()
        print(f"Error importing data: {e}")
        raise
    finally:
        db.close()

if __name__ == '__main__':
    import_base_xlsx()
