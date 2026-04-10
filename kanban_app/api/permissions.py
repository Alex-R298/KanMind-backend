"""Custom permissions for the Kanban app."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    """Allow read for all authenticated users, write only for author."""

    def has_object_permission(self, request, view, obj):
        """Return True for safe methods or if user is the author."""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
