"""Custom permissions for the Kanban app."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    """Allow read for all authenticated users, write only for author."""

    def has_object_permission(self, request, view, obj):
        """Return True for safe methods or if user is the author."""
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsBoardMember(BasePermission):
    """Allow access only if user is board owner or member."""

    def has_object_permission(self, request, view, obj):
        """Return True if user is author or member of the board."""
        return (
            obj.author == request.user
            or obj.members.filter(pk=request.user.pk).exists()
        )
