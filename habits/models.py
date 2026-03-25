from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

class CustomUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    telegram_chat_id = models.BigIntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.username

class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to'
    )
    periodicity = models.IntegerField(default=1)
    reward = models.CharField(max_length=255, blank=True)
    execution_time = models.DurationField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.execution_time > timedelta(seconds=120):
            raise ValidationError('Время выполнения не может быть больше 120 секунд')
        if not (1 <= self.periodicity <= 7):
            raise ValidationError('Периодичность должна быть от 1 до 7 дней')
        if self.is_pleasant:
            if self.reward:
                raise ValidationError('Приятная привычка не может иметь вознаграждения')
            if self.related_habit:
                raise ValidationError('Приятная привычка не может иметь связанной привычки')
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя одновременно указать вознаграждение и связанную привычку')
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.place}"
