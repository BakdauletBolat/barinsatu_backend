from rest_framework import permissions

class AuthorPermission(permissions.BasePermission):

    message = "You dont have Permission Дурак"

    def has_object_permission(self, request,view,obj):
        user = request.user
        return user == obj.author

class IsSuperUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)