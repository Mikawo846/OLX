import asyncio
from telegram_notifier import TelegramNotifier
from database import SessionLocal, ReferenceModel
import config

async def test_telegram():
    print("Testing Telegram Notifier...")
    print("=" * 80)
    
    if not config.TELEGRAM_BOT_TOKEN:
        print("\n⚠️  TELEGRAM_BOT_TOKEN not set in .env")
        print("Please configure your Telegram bot token first.")
        return
    
    if not config.TELEGRAM_CHAT_ID:
        print("\n⚠️  TELEGRAM_CHAT_ID not set in .env")
        print("Please configure your Telegram chat ID first.")
        return
    
    print(f"\nBot Token: {config.TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"Chat ID: {config.TELEGRAM_CHAT_ID}")
    
    db = SessionLocal()
    model = db.query(ReferenceModel).first()
    
    if not model:
        print("\n⚠️  No models in database!")
        print("Run: python import_base.py")
        db.close()
        return
    
    print(f"\nUsing test model: {model.brand} {model.model_name}")
    
    test_ad = {
        'id': 'test_12345',
        'title': f'{model.brand} {model.model_name} в отличном состоянии',
        'price': model.base_price * 0.7,
        'url': 'https://www.olx.kz/d/test-ad',
        'location': 'Алматы, Бостандыкский район',
        'image_url': 'https://via.placeholder.com/300x200.png?text=Test+Camera',
        'category': 'camera'
    }
    
    deal_info = {
        'discount_percent': 30.0,
        'savings': model.base_price * 0.3,
        'ad_price': test_ad['price'],
        'base_price': model.base_price,
        'threshold_price': model.base_price * 0.8
    }
    
    print("\nSending test notification...")
    print("Check your Telegram for the message!\n")
    
    notifier = TelegramNotifier()
    success = await notifier.send_deal_notification(test_ad, model, deal_info)
    
    if success:
        print("✓ Test notification sent successfully!")
    else:
        print("✗ Failed to send notification. Check logs for errors.")
    
    db.close()

if __name__ == '__main__':
    asyncio.run(test_telegram())
