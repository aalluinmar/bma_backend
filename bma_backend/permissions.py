from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """
    Custom permissions for all the users.
    1. Only Admin User can perform all the user operations.
    2. Requested user can only get/update their self details.
    3. User creation API will be called only once if the user doesn't exist.
    """

    def has_permission(self, request, view):
        # User creation API will be called only once if the user doesn't exist
        if (request.method == "POST" and (not request.user.id)):
            return True
        elif not request.user.id:  # If the requested user doesn't exist
            return False
        elif (
                (hasattr(request.user, "is_superuser") and request.user.is_superuser)
                    or
                (hasattr(request.user, "is_admin") and request.user.is_admin)
            ):  # Only superuser/admin can perform all actions w.r.t users View
            return True
        elif (request.method in ["GET", "PUT", "PATCH"] and view and view.get_object()
                and request.user.id == view.get_object().id):
            # If Requested user tries to make themselves as Admin then return False
            if request.data.get("is_admin", False):
                return False
            # Only the requested user can see their self details but not other user details
            return True
        return False  # Returns False if request doesn't fit.
