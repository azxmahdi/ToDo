from rest_framework.permissions import BasePermission, SAFE_METHODS


class DefaultPermission(BasePermission):
    """
    Custom permission class for the ToDo API.

    This class provides object-level permissions for the ToDo objects.
    It allows read access to all requests, but only allows write access to the objects
    owned by the authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine if the user has permission to perform the requested action on the given object.

        Args:
        - request: The incoming request object.
        - view: The view on which the permission check is being performed.
        - obj: The specific ToDo object being accessed.

        Returns:
        - True if the user has permission to perform the requested action on the given object.
        - False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
