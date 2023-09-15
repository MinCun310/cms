from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.hashers import check_password

from ..serializers import SecuritySerializer
from ..models import UserModel
from ..config.constants import ERROR_CODE

class SecurityView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = SecuritySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        password = user.password
        new_password = serializer.data["new_password"]
        old_password = serializer.data["old_password"]
        print(password)
        print(old_password)
        
        if check_password(old_password, password):
            if old_password == new_password:
                return Response({
                    "status": False,
                    "message": "Password should not be same with old password",
                    "ERROR_CODE": ERROR_CODE["OLD_NEW_PASSWORD_NOT_SAME"]
                })
            else:
                user.set_password(new_password)
                user.save()
                return Response({
                    "message": "password is changed successfully"
                })
        else:
            return Response({
            "message": "Password is incorrected",
            "ERROR_CODE": ERROR_CODE["OLD_PASSWORD_NOT_CORRECT"]
        })