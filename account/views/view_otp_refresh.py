from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from ..serializers import OTPRefreshSerializer
from ..models import UserModel
from ..libs.ticket import take_user_id_from_ticket, generate_ticket

from ..libs.device import store_device
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp
from ..config.constants import ERROR_CODE
from ..libs.ticket import ticket_is_expired, ticket_is_invalid
from django_ratelimit.decorators import ratelimit
from smtplib import SMTPException
from django.utils.decorators import method_decorator
from django.core.cache import cache


@method_decorator(ratelimit(key="user_or_ip", rate="1/m"), name="post")
class OTPRefreshView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        ticket = request.data.get("ticket")
        if ticket_is_invalid(ticket):
            return Response(
                {
                    "status": False,
                    "message": "Ticket is invalid",
                    "error_code": ERROR_CODE["TICKET_INVALID"],
                },
                status.HTTP_400_BAD_REQUEST,
            )
        if ticket_is_expired(ticket):
            return Response(
                {
                    "status": False,
                    "message": "Ticket is expired",
                    "error_code": ERROR_CODE["TICKET_EXPIRED"],
                },
                status.HTTP_400_BAD_REQUEST,
            )

        serializer = OTPRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        # timeout = cache.ttl(data["ticket"])
        # print(51, timeout)
        user_id = take_user_id_from_ticket(data["ticket"])
        user = UserModel.objects.get(id=user_id)

        # if timeout != 0:
        #     return Response(
        #         {
        #             "ticket": data["ticket"],
        #             "timeout": timeout,
        #             "error_code": ERROR_CODE["TICKET_EXPIRED"],
        #         },
        #         status.HTTP_400_BAD_REQUEST,
        #     )

        device = store_device(request, user)
        new_ticket = generate_ticket(user, device)
        code = generate_otp_code()
        print("resend code: ", code)
        try:
            send_mail_with_otp(code, user.email)
            cache.set(new_ticket, code, timeout=60)
        except SMTPException:
            return Response(
                {
                    "message": "Error sending OTP",
                    "error_code": ERROR_CODE["SEND_OTP_ERROR"],
                },
                status.HTTP_400_BAD_REQUEST,
            )
        return Response({"has_otp": True, "ticket": new_ticket})
