from rest_framework import serializers
from datetime import timedelta


def validate_execution_time(value):
    if value > timedelta(seconds=120):
        raise serializers.ValidationError('Время выполнения не может быть больше 120 секунд')
    return value

def validate_periodicity(value):
    if not (1 <= value <= 7):
        raise serializers.ValidationError('Периодичность должна быть от 1 до 7 дней')
    return value
