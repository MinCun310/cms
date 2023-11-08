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
from ..models import BlacklistedTokenModel

from ..config.constants import ERROR_CODE


class OTPVerifyView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        code = cache.get(data["ticket"])

        if code is None:
            return Response(
                {"message": "Code is expired", "error_code": ERROR_CODE["OTP_EXPIRED"]},
                status.HTTP_400_BAD_REQUEST,
            )

        if code != data["code"]:
            return Response(
                {
                    "message": "Invalid OTP code",
                    "error_code": ERROR_CODE["OTP_INVALID"],
                },
                status.HTTP_400_BAD_REQUEST,
            )

        user_id = take_user_id_from_ticket(data["ticket"])
        user = UserModel.objects.get(pk=user_id)

        cache.delete(data["ticket"])

        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        access = str(refresh.access_token)
        return Response(
            {
                "status": "verified",
                "user": user_serializer.data,
                "token": {"refresh": str(refresh), "access": access},
            }
        )
