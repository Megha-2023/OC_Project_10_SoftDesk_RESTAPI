from rest_framework.permissions import BasePermission


class ProjectAuthentication(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            return bool(request.user in obj.contributors.all())
        return bool(obj.author == request.user)
    