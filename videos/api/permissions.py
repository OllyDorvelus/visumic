from rest_framework import permissions


class MyUserPermissions(permissions.BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
     """

    def has_object_permission(self, request, view, obj):

        # check if user is owner
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class UserAddOrRemovePermissions(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        return request.user == obj.user


class UserAndVideoUserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # check if user is owner
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user or request.user == obj.video.user or request.user == obj.parent.user