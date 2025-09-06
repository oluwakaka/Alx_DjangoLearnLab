from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only methods for everyone, but write methods only for the object's owner.
    Assumes the object has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write: only the author can modify/delete
        return getattr(obj, "author", None) == request.user
