import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

test_urls = [
    'https://www.olx.kz/api/v1/offers/?offset=0&limit=40&category_id=1107',
    'https://www.olx.kz/d/api/v1/offers-listing/?offset=0&limit=40&category_id=1107',
]

print("Проверка API эндпоинтов OLX...\n")

for url in test_urls:
    print(f"Пробую: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✓ JSON получен! Ключи: {list(data.keys())[:5]}")
                
                if 'data' in data:
                    print(f"  Найдено объявлений: {len(data.get('data', []))}")
                    if data.get('data'):
                        first_ad = data['data'][0]
                        print(f"  Пример: {first_ad.get('title', 'N/A')[:50]}")
                
                print(f"\nПолный ответ (первые 500 символов):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                print("\n" + "="*80 + "\n")
                break
            except:
                print(f"  Не JSON ответ")
        else:
            print(f"  Ошибка HTTP")
    except Exception as e:
        print(f"  Ошибка: {e}")
    print()

print("\nПопробуем загрузить обычную страницу и найти данные...")
response = requests.get('https://www.olx.kz/elektronika/foto-video/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Длина HTML: {len(response.text)}")

if '__PRELOADED_STATE__' in response.text:
    print("✓ Найден __PRELOADED_STATE__ - данные есть в HTML!")
    start = response.text.find('__PRELOADED_STATE__')
    snippet = response.text[start:start+200]
    print(f"Фрагмент: {snippet}")
elif 'window.__INITIAL_STATE__' in response.text:
    print("✓ Найден window.__INITIAL_STATE__")
else:
    print("✗ Данные не найдены в HTML")
