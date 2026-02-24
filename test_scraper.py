import logging
from olx_scraper import OLXScraper
import config

logging.basicConfig(level=logging.INFO)

def test_scraper():
    print("Testing OLX Scraper...")
    print("=" * 80)
    
    scraper = OLXScraper()
    
    test_category = config.OLX_CATEGORIES[0]
    print(f"\nTesting category: {test_category['name']}")
    print(f"URL: {test_category['url']}")
    print(f"Category ID: {test_category['category_id']}")
    print("\nFetching ads (1 page only)...\n")
    
    ads = scraper.fetch_ads(test_category['url'], test_category['category_id'], max_pages=1)
    
    print(f"\n{'=' * 80}")
    print(f"Found {len(ads)} ads")
    print(f"{'=' * 80}\n")
    
    if ads:
        print("Sample ads:\n")
        for i, ad in enumerate(ads[:5], 1):
            print(f"{i}. {ad['title']}")
            print(f"   Price: {ad['price']} {ad['currency']}")
            print(f"   URL: {ad['url']}")
            print(f"   Location: {ad['location']}")
            print(f"   ID: {ad['id']}")
            print()
    else:
        print("No ads found. This might indicate:")
        print("1. OLX changed their HTML structure")
        print("2. Network issues")
        print("3. The category has no listings")
        print("\nCheck olx_scraper.py selectors if needed.")

if __name__ == '__main__':
    test_scraper()
