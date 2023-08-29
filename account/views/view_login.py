from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers import LoginSerializer,DeviceSerializer
from ..libs.device import store_device
from ..models import UserModel

permission_class = [AllowAny, ]

class LoginView(APIView):

    # @method_decorator(respond_immediately_if_user_is_logged_in)
    def post(self, request):
        # 1. validate data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 2. kiểm tra xem thông tin username và password có hợp lệ hay không
        credentials = serializer.validated_data
        user = authenticate(**credentials)
        if user is None:
            return Response({
                "Message": "The username or password is incorrect",
            }, status=status.HTTP_400_BAD_REQUEST )
        
        store_device(request, user)
        # print('device_info', device)
        
        return Response({
            "data": {
                "data": serializer.data,
            }
        })
        