from celery import shared_task
from datetime import datetime
from habits.models import Habit
from telegram_bot.bot import bot
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_habit_reminder():
    """Задача Celery для отправки напоминаний о привычках"""
    now = datetime.now().time()

    habits_to_remind = Habit.objects.filter(
        time__hour=now.hour, time__minute=now.minute
    )

    for habit in habits_to_remind:
        if habit.user.telegram_chat_id:
            message = (
                f"⏰ Напоминание: пора выполнить привычку!\n\n"
                f"{habit.action}\n"
                f"Место: {habit.place}\n"
                f"Время: {habit.time}"
            )
            try:
                bot.send_message(habit.user.telegram_chat_id, message)
                logger.info(f"Напоминание отправлено пользователю {habit.user.user.id}")
            except Exception as e:
                logger.error(
                    f"Ошибка отправки напоминания для пользователя {habit.user.user.id}: {e}"
                )
