import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

urls_to_check = {
    'foto-video': 'https://www.olx.kz/elektronika/foto-video/',
    'telefony': 'https://www.olx.kz/elektronika/telefony-i-aksesuary/',
    'smartfony': 'https://www.olx.kz/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/',
    'kompyutery': 'https://www.olx.kz/elektronika/kompyutery-i-komplektuyuschie/',
    'planshety': 'https://www.olx.kz/elektronika/planshety-el-knigi-i-aksessuary/planshetnye-kompyutery/',
    'igry': 'https://www.olx.kz/elektronika/igry-i-igrovye-pristavki/',
}

print("Поиск category_id для каждой категории...\n")

for name, url in urls_to_check.items():
    print(f"{name}: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        import re
        match = re.search(r'"category_id["\s:]+(\d+)', html)
        if match:
            cat_id = match.group(1)
            print(f"  ✓ category_id: {cat_id}")
            
            api_url = f"https://www.olx.kz/api/v1/offers/?offset=0&limit=5&category_id={cat_id}"
            api_response = requests.get(api_url, headers=headers, timeout=10)
            if api_response.status_code == 200:
                data = api_response.json()
                ads = data.get('data', [])
                if ads:
                    print(f"  ✓ API работает! Найдено {len(ads)} объявлений")
                    print(f"    Пример: {ads[0].get('title', '')[:60]}")
            else:
                print(f"  ✗ API не работает")
        else:
            print(f"  ✗ category_id не найден")
    except Exception as e:
        print(f"  ✗ Ошибка: {e}")
    print()
