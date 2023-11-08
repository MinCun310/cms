from rest_framework.permissions import BasePermission


# https://www.django-rest-framework.org/api-guide/permissions/
class OnlyOwnerAccessIt(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return obj.id == request.user.id

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
