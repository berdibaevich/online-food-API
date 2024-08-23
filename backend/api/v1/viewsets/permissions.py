from rest_framework import generics
from rest_framework.permissions import BasePermission


class MixedPermission(generics.GenericAPIView):
    """
        Mixed Permission for action
    """
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]




class IsOwnerOfProfile(BasePermission):
    """
        For profile permission, if user is authenticated and 
        owner of profile
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.pk



class AdminDashboardPermission(BasePermission):
    """
        Only Admin for admin dashboard :)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_superuser