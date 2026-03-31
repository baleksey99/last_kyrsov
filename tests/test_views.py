from django.test import TestCase
from django.contrib.auth.models import User
from habits.models import Habit, UserProfile
from datetime import time, timedelta
from rest_framework import status


class HabitViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)


        login_success = self.client.login(username="testuser", password="12345")
        if not login_success:
            self.fail("Авторизация в setUp не удалась")


        response = self.client.get(
            "/api/auth/current-user/"
        )
        print("Authorization check response:", response.status_code, response.content)


        self.habit = Habit.objects.create(
            user=self.user_profile,
            place="Офис",
            time=time(18, 0),
            action="Прогулка",
            is_pleasant=False,
            periodicity=1,
            reward="Отдых",
            execution_time=timedelta(seconds=120),
            is_public=True,
        )

    def test_habits_list_view(self):
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, 200)

        try:
            response_data = response.json()
            if "results" in response_data:
                habits = response_data["results"]
            else:
                habits = response_data
            self.assertGreaterEqual(len(habits), 1)
        except ValueError:
            self.fail("Ответ не в формате JSON")

    def test_habit_detail_404(self):
        """Тест доступа к несуществующей привычке"""
        response = self.client.get("/habits/999/")
        self.assertEqual(response.status_code, 404)

    def test_habit_list_filtering_by_pleasant(self):
        """Тест фильтрации привычек по is_pleasant"""
        response = self.client.get("/api/habits/?is_pleasant=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_detail_not_found(self):
        """Тест доступа к несуществующей привычке"""
        response = self.client.get("/api/habits/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
