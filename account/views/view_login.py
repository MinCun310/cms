from django.core.cache import cache

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers import LoginSerializer
from ..serializers import LoginSerializer, DeviceSerializer

from smtplib import SMTPException

from ..libs.device import store_device
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp
from ..libs.ticket import generate_ticket
from ..config.constants import ERROR_CODE

permission_class = [
    AllowAny,
]


class LoginView(APIView):
    def post(self, request):
        # 1. validate data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # print(serializer.data["password"])

        # 2. kiểm tra xem thông tin username và password có hợp lệ hay không
        credentials = serializer.validated_data
        user = authenticate(**credentials)
        if user is None:
            return Response(
                {
                    "message": "The username or password is incorrect",
                    "error_code": ERROR_CODE["USERNAME_PASSWORD_INCORECT"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        device = store_device(request, user)
        # print('device_info', device)
        ticket = generate_ticket(user, device)
        print("---------------------")
        print("ticket: ", ticket)
        code = generate_otp_code()
        print("---------------------")
        print("code: ", code)
        print("session_id", request.session.session_key)
        try:
            send_mail_with_otp(code, user.email)
            cache.set(ticket, code, timeout=60)
            print(cache.get(ticket))
            # key ticket value otp set time 60s
        except SMTPException:
            return Response(
                {
                    "status": True,
                    "message": "Error sending OTP",
                    "error_code": ERROR_CODE["SEND_OTP_ERROR"],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # save ticket in cache
        return Response(
            {"has_otp": True, "message": "Email verify required", "ticket": ticket}
        )
