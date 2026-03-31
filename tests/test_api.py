from django.test import TestCase
from django.contrib.auth.models import User
from habits.models import Habit, UserProfile
from datetime import time, timedelta
import json
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)


        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_create_habit(self):
        data = {
            "place": "Парк",
            "time": "08:00:00",
            "action": "Бег",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": "00:01:00",
        }
        response = self.client.post("/api/habits/", data, format="json")
        self.assertEqual(response.status_code, 201)

    def tearDown(self):

        self.client.credentials()

    def test_get_habits_list(self):

        habit = Habit.objects.create(
            user=self.user_profile,
            place="Парк",
            time=time(10, 0),
            action="Бег",
            is_pleasant=True,
            execution_time=timedelta(seconds=60),
        )

        response = self.client.get("/api/habits/")
        print("Status code:", response.status_code)

        try:
            response_data = response.json()
            print("Full response:", response_data)


            if "results" in response_data:
                habits = response_data["results"]
                print("Habits from 'results':", habits)
            else:
                habits = response_data
                print("Habits (direct):", habits)

        except ValueError:
            self.fail("Ответ не в формате JSON")

    def test_list_habits_filtering(self):
        """Тест фильтрации списка привычек"""
        response = self.client.get("/api/habits/?is_pleasant=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
