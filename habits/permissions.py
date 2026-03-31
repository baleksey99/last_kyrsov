from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ только владельцу привычки.
    Для остальных — только чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Только владелец может редактировать/удалять
        return obj.user == request.user
