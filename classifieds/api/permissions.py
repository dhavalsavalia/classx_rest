from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPosterOrReadOnly(BasePermission):
    """
    The request is authenticated as a poster(the one who posted the item), or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj.user == request.user
        )
