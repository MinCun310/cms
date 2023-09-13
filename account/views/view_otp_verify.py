# from django.utils.decorators import method_decorator
from django.core.cache import cache

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import OTPVerifySerializer, UserSerializer

from ..libs.ticket import take_user_id_from_ticket

from ..models import UserModel

from ..config.constants import ERROR_CODE

class OTPVerifyView(APIView):
    permission_classes = [AllowAny, ]
    
    # @method_decorator(response_immediately_if_user_is_logged_in)
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        code = cache.get(data["ticket"])
        
        if code == None:
            return Response ({
                "message": "Code is expired",
                'error_code': ERROR_CODE['OTP_EXPIRED']
            }, status.HTTP_400_BAD_REQUEST)
            
        if code != data["code"]:
            return Response ({
                "message": "Invalid OTP code",
                'error_code': ERROR_CODE['OTP_INVALID']
            }, status.HTTP_400_BAD_REQUEST)
            
        UserId = take_user_id_from_ticket(data["ticket"])
        user = UserModel.objects.get(pk=UserId)
        
        cache.delete(data["ticket"])
        
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        
        return Response({
            'status': "verified",
            'user': user_serializer.data,
            "token": {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        })