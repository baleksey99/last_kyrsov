from django.test import TestCase
from datetime import timedelta
from habits.models import UserProfile, Habit
from django.contrib.auth.models import User


class HabitModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user)

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.profile,
            action="Утренняя зарядка",
            place="Дома",
            time="08:00:00",
            execution_time=timedelta(seconds=120),
            is_pleasant=True,
            periodicity=1,
            reward="",
            is_public=False,
        )
        self.assertEqual(habit.action, "Утренняя зарядка")
        self.assertEqual(habit.place, "Дома")
        self.assertEqual(habit.execution_time.seconds, 120)

    def test_execution_time_validation(self):
        """Проверка валидации времени выполнения"""
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.profile,
                action="Долгая привычка",
                place="Офис",
                time="09:00:00",
                execution_time=timedelta(minutes=30),  # > 120 сек
                is_pleasant=False,
                periodicity=3,
                reward="Кофе",
                is_public=True,
            )

    def test_profile_user_relation(self):
        """Проверка связи профиля с пользователем"""
        self.assertEqual(self.profile.user.username, "testuser")
