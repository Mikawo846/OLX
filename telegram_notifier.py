import asyncio
from telegram import Bot
from telegram.error import TelegramError
from telegram.request import HTTPXRequest
import logging
from typing import Dict
import config
from database import ReferenceModel

logger = logging.getLogger(__name__)

class TelegramNotifier:
    def __init__(self):
        if not config.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram bot token not configured")
            self.bot = None
        else:
            request = HTTPXRequest(
                connection_pool_size=8,
                connect_timeout=30.0,
                read_timeout=30.0,
                write_timeout=30.0,
                pool_timeout=30.0
            )
            self.bot = Bot(token=config.TELEGRAM_BOT_TOKEN, request=request)
        
        self.chat_id = config.TELEGRAM_CHAT_ID
    
    async def send_deal_notification(self, ad: Dict, model: ReferenceModel, deal_info: Dict):
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured, skipping notification")
            return False
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                message = self._format_message(ad, model, deal_info)
                
                if ad.get('image_url'):
                    try:
                        await self.bot.send_photo(
                            chat_id=self.chat_id,
                            photo=ad['image_url'],
                            caption=message,
                            parse_mode='HTML'
                        )
                    except Exception as img_error:
                        logger.warning(f"Failed to send image, sending text only: {img_error}")
                        await self.bot.send_message(
                            chat_id=self.chat_id,
                            text=message,
                            parse_mode='HTML',
                            disable_web_page_preview=False
                        )
                else:
                    await self.bot.send_message(
                        chat_id=self.chat_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=False
                    )
                
                logger.info(f"Notification sent for ad {ad['id']}")
                return True
                
            except TelegramError as e:
                logger.error(f"Telegram error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return False
            except Exception as e:
                logger.error(f"Error sending notification (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    return False
        
        return False
    
    def _format_message(self, ad: Dict, model: ReferenceModel, deal_info: Dict) -> str:
        discount = deal_info['discount_percent']
        savings = deal_info['savings']
        
        message = f"🔥 <b>ВЫГОДНОЕ ПРЕДЛОЖЕНИЕ!</b>\n\n"
        message += f"📱 <b>{model.brand} {model.model_name}</b>\n\n"
        message += f"💰 Цена: <b>{int(ad['price'])} ₸</b>\n"
        message += f"📊 Базовая цена: <s>{int(model.base_price)} ₸</s>\n"
        message += f"🎯 Скидка: <b>{discount:.1f}%</b>\n"
        message += f"💵 Экономия: <b>{int(savings)} ₸</b>\n\n"
        
        if ad.get('location'):
            message += f"📍 {ad['location']}\n"
        
        message += f"\n🔗 <a href='{ad['url']}'>Открыть объявление</a>\n"
        message += f"\n<i>{ad['title']}</i>"
        
        return message
    
    def send_notification_sync(self, ad: Dict, model: ReferenceModel, deal_info: Dict):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.send_deal_notification(ad, model, deal_info))
