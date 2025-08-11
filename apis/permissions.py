from rest_framework.permissions import BasePermission


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        permission_types = {
            "list": "view",
            "retrieve": "view",
            "create": "add",
            "update": "change",
            "partial_update": "change",
            "destroy": "delete",
        }

        access_type = permission_types.get(view.action)
        if not access_type:
            return False

        permission_to_look = f"{access_type}_{view.basename}"

        return request.user.groups.filter(
            permissions__codename=permission_to_look
        ).exists()
