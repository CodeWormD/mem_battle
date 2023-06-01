from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def is_authenticated(self, request):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_superuser
                    or request.user.is_authenticated))

    def has_permission(self, request, view):
        # print(f'VIEW - {view.__dict__}')
        return self.is_authenticated(request)

    def has_object_permission(self, request, view, obj):
        # print(f'OBJ - {obj}')
        return (request.method in permissions.SAFE_METHODS or
                (request.user.is_superuser or request.user == obj.owner))