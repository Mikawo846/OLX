import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

test_queries = [
    ('Canon', 'фотоаппарат'),
    ('Nikon', 'камера'),
    ('iPhone', 'телефон'),
    ('Samsung', 'смартфон'),
]

print("Тестирование поиска OLX API...\n")

for brand, category in test_queries:
    query = f"{brand} {category}"
    api_url = f"https://www.olx.kz/api/v1/offers/?offset=0&limit=10&query={query}"
    
    print(f"Поиск: '{query}'")
    print(f"URL: {api_url}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            ads = data.get('data', [])
            print(f"✓ Найдено: {len(ads)} объявлений")
            
            if ads:
                for i, ad in enumerate(ads[:3], 1):
                    title = ad.get('title', '')
                    params = ad.get('params', [])
                    price = 0
                    for p in params:
                        if p.get('key') == 'price':
                            pv = p.get('value', {})
                            if isinstance(pv, dict):
                                price = pv.get('value', 0)
                    
                    print(f"  {i}. {title[:50]} - {price} тг")
        else:
            print(f"✗ HTTP {response.status_code}")
    except Exception as e:
        print(f"✗ Ошибка: {e}")
    print()

print("\n" + "="*80)
print("Проверка фильтра по категории в поиске...")
print("="*80 + "\n")

search_with_filter = "https://www.olx.kz/api/v1/offers/?offset=0&limit=10&query=Canon&filter_refiners=category_without_exclusions"

response = requests.get(search_with_filter, headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"Ключи ответа: {list(data.keys())}")
    if 'metadata' in data:
        print(f"Metadata: {json.dumps(data['metadata'], indent=2, ensure_ascii=False)[:500]}")
