import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

DISCOUNT_THRESHOLD = float(os.getenv('DISCOUNT_THRESHOLD', '0.20'))
MIN_REAL_PRICE = float(os.getenv('MIN_REAL_PRICE', '1000'))
SCRAPE_INTERVAL_SECONDS = int(os.getenv('SCRAPE_INTERVAL_SECONDS', '300'))

IGNORE_WORDS = os.getenv('IGNORE_WORDS', '').split(',')

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///olx_parser.db')

OLX_CATEGORIES = [
    {
        'name': 'foto-video',
        'url': 'https://www.olx.kz/elektronika/foto-video/',
        'category_id': 'camera'
    },
    {
        'name': 'telefony-i-aksesuary',
        'url': 'https://www.olx.kz/elektronika/telefony-i-aksesuary/',
        'category_id': 'phone'
    },
    {
        'name': 'mobilnye-telefony-smartfony',
        'url': 'https://www.olx.kz/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/',
        'category_id': 'smartphone'
    },
    {
        'name': 'kompyutery-i-komplektuyuschie',
        'url': 'https://www.olx.kz/elektronika/kompyutery-i-komplektuyuschie/',
        'category_id': 'computer'
    },
    {
        'name': 'planshetnye-kompyutery',
        'url': 'https://www.olx.kz/elektronika/planshety-el-knigi-i-aksessuary/planshetnye-kompyutery/',
        'category_id': 'tablet'
    },
    {
        'name': 'igry-i-igrovye-pristavki',
        'url': 'https://www.olx.kz/elektronika/igry-i-igrovye-pristavki/',
        'category_id': 'gaming'
    }
]

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5
