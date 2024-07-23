from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Only a contact owner can perform CRUD operations on it.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # print(f"obj owner: {obj.owner} | request user: {request.user}")
        return obj.owner == request.user


class IsUser(permissions.BasePermission):
    """
    Only a user can view their own profile.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id