from rest_framework import serializers
from .models import Habit
from .validators import validate_execution_time, validate_periodicity


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "execution_time",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["user"]

    def validate(self, data):
        execution_time = data.get("execution_time")
        if execution_time:
            validate_execution_time(execution_time)

        periodicity = data.get("periodicity")
        if periodicity:
            validate_periodicity(periodicity)

        is_pleasant = data.get("is_pleasant")
        reward = data.get("reward")
        related_habit = data.get("related_habit")

        if is_pleasant:
            if reward:
                raise serializers.ValidationError(
                    "Приятная привычка не может иметь вознаграждения"
                )
            if related_habit:
                raise serializers.ValidationError(
                    "Приятная привычка не может иметь связанной привычки"
                )

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку"
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")

        return data
