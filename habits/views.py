from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
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
            # Возвращаем привычки пользователя + все публичные
            return Habit.objects.filter(
                Q(user__user=user) | Q(is_public=True)
            )
        else:
            # Анонимный пользователь видит только публичные привычки
            return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        # Получаем CustomUser для текущего пользователя
        custom_user = UserProfile.objects.get(user=self.request.user)
        serializer.save(user=custom_user)

    @action(detail=False, methods=['get'])
    def my_habits(self, request):
        """Список привычек текущего пользователя"""
        habits = Habit.objects.filter(user__user=request.user)
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Список публичных привычек"""
        public_habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(public_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)
