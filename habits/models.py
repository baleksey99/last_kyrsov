from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


class Habit(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="habits"
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.TextField(verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )
    periodicity = models.IntegerField(default=1, verbose_name="Периодичность (дней)")
    reward = models.CharField(max_length=255, blank=True, verbose_name="Вознаграждение")
    execution_time = models.DurationField(verbose_name="Время выполнения")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    def clean(self):
        if isinstance(self.execution_time, str):
            try:
                parts = self.execution_time.split(":")
                if len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                else:
                    hours, minutes, seconds = 0, int(parts[0]), int(parts[1])
                self.execution_time = timedelta(
                    hours=hours, minutes=minutes, seconds=seconds
                )
            except (ValueError, IndexError):
                raise ValidationError("Неверный формат времени выполнения")

        max_execution_time = timedelta(seconds=120)
        if self.execution_time > max_execution_time:
            raise ValidationError("Время выполнения не может быть больше 120 секунд")

        max_execution_time = timedelta(seconds=120)
        if self.execution_time > max_execution_time:
            raise ValidationError("Время выполнения не может быть больше 120 секунд")

        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")

        if self.is_pleasant:
            if self.reward:
                raise ValidationError("Приятная привычка не может иметь вознаграждения")
            if self.related_habit:
                raise ValidationError(
                    "Приятная привычка не может иметь связанной привычки"
                )

        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку"
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

        if self.related_habit == self:
            raise ValidationError("Привычка не может быть связана сама с собой")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]
