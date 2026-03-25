from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from habits.models import Habit, CustomUser
import json

class HabitAPITest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.custom_user = CustomUser.objects.create(user=self.user)
        self.client.login(username='testuser', password='12345')

        # Создаём тестовую привычку
        self.habit = Habit.objects.create(
            user=self.custom_user,
            place='Дом',
            time='09:00:00',
            action='Зарядка',
            is_pleasant=False,
            periodicity=1,
            reward='Чашка кофе',
            execution_time='00:01:00',  # 1 минута
            is_public=True
        )

    def test_get_habits_list(self):
        response = self.client.get(reverse('habit-list'))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_habit(self):
        data = {
            'place': 'Офис',
            'time': '18:00:00',
            'action': 'Прогулка',
            'is_pleasant': False,
            'periodicity': 1,
            'reward': 'Отдых',
            'execution_time': '00:02:00',
            'is_public': True
        }
        response = self.client.post(reverse('habit-list'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 2)

    def test_my_habits_endpoint(self):
        response = self.client.get('/api/habits/my_habits/')
        self.assertEqual(response.status_code, 200)
