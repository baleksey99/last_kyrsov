import logging
from telegram.ext import Application
from decouple import config

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    def send_message(self, chat_id: int, text: str):
        """Отправка сообщения пользователю"""
        try:
            self.application.bot.send_message(chat_id=chat_id, text=text)
            logger.info(f"Сообщение отправлено пользователю {chat_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения {chat_id}: {e}")


# Глобальный экземпляр бота
bot = TelegramBot()
