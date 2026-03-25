from django.contrib.auth.models import User
from habits.models import CustomUser

def link_telegram_user(user: User, telegram_chat_id: int):
    """Привязка Telegram‑пользователя к Django‑аккаунту"""
    try:
        custom_user = CustomUser.objects.get(user=user)
    except CustomUser.DoesNotExist:
        custom_user = CustomUser.objects.create(user=user)

    custom_user.telegram_chat_id = telegram_chat_id
    custom_user.save()
    return True


def unlink_telegram_user(user: User):
    """Отвязка Telegram‑пользователя"""
    try:
        custom_user = CustomUser.objects.get(user=user)
        custom_user.telegram_chat_id = None
        custom_user.save()
        return True
    except CustomUser.DoesNotExist:
        return False

def get_telegram_chat_id(user: User) -> int | None:
    """Получение Telegram chat_id для пользователя"""
    try:
        custom_user = CustomUser.objects.get(user=user)
        return custom_user.telegram_chat_id
    except CustomUser.DoesNotExist:
        return None
