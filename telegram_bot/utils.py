from django.contrib.auth.models import User
from habits.models import UserProfile


def link_telegram_user(user: User, telegram_chat_id: int):
    """Привязка Telegram‑пользователя к Django‑аккаунту"""
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    user_profile.telegram_chat_id = telegram_chat_id
    user_profile.save()
    return True


def unlink_telegram_user(user: User):
    """Отвязка Telegram‑пользователя"""
    try:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.telegram_chat_id = None
        user_profile.save()
        return True
    except UserProfile.DoesNotExist:
        return False


def get_telegram_chat_id(user: User) -> int | None:
    """Получение Telegram chat_id для пользователя"""
    try:
        user_profile = UserProfile.objects.get(user=user)
        return user_profile.telegram_chat_id
    except UserProfile.DoesNotExist:
        return None
