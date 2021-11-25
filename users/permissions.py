from rest_framework.permissions import BasePermission

class IsSelf(BasePermission):
    def has_object_permission(self, request, view, user):
        print(user)
        return user == request.user