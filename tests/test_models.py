from django.test import TestCase
from django.utils import timezone
from datetime import time, timedelta
from habits.models import Habit, CustomUser
from django.contrib.auth.models import User

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.custom_user = CustomUser.objects.create(user=self.user)

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.custom_user,
            place='Дом',
            time=time(9, 0),
            action='Зарядка',
            is_pleasant=False,
            periodicity=1,
            reward='Чашка кофе',
            execution_time=timedelta(seconds=60),
            is_public=True
        )
        self.assertEqual(habit.action, 'Зарядка')
        self.assertEqual(habit.place, 'Дом')

    def test_execution_time_validation(self):
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.custom_user,
                place='Дом',
                time=time(9, 0),
                action='Долгое действие',
                is_pleasant=False,
                periodicity=1,
                reward='',
                execution_time=timedelta(seconds=130),  # > 120 секунд
                is_public=False
            )
