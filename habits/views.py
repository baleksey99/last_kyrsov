from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Habit, UserProfile
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(
                Q(user__user=user) | Q(is_public=True)
            ).select_related("user", "related_habit")
        else:
            return Habit.objects.filter(is_public=True).select_related(
                "user", "related_habit"
            )

    def perform_create(self, serializer):
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=self.request.user)

        serializer.save(user=user_profile)

    @action(detail=False, methods=["get"])
    def my_habits(self, request):
        """Список привычек текущего пользователя"""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            user_profile = UserProfile.objects.get(user=request.user)
            habits = Habit.objects.filter(user=user_profile).select_related(
                "related_habit"
            )
            serializer = self.get_serializer(habits, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "Профиль пользователя не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"])
    def public(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True).select_related(
            "user", "related_habit"
        )
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)
