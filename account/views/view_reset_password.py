from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# from ..models.model_user import OldPasswords

from smtplib import SMTPException
from django.contrib.auth.hashers import check_password, make_password
from ..serializers import SendMailToResetPasswordSerializer, ResetPasswordSerializer
from ..models.model_user import UserModel

# from ..models.model_device import DeviceModel
from ..config.constants import ERROR_CODE
from ..libs.ticket import generate_ticket, take_user_id_from_ticket
from ..libs.mail import send_mail_with_link_reset_password


class SendMailToResetPasswordView(APIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = SendMailToResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(20, serializer.data["email"])
        user = UserModel.objects.get(email=serializer.data["email"])

        # device = DeviceModel.objects.filter(user_id=user.id)
        # print("Xem thử--->", device)
        # device_dict = dict(device.values()[device.count()-1])
        # print(20, device_dict)
        # ticket = generate_ticket(user=user, device=device_dict)
        ticket = generate_ticket(user=user)
        print("ticket", ticket)
        try:
            # send_mail_with_link_reset_password(user, device_dict['ip'], ticket)
            send_mail_with_link_reset_password(
                user, request.META["REMOTE_ADDR"], ticket
            )
        except SMTPException:
            return Response(
                {
                    "status": False,
                    "message": "Email had some error when send",
                    "error_code": ERROR_CODE["SEND_MAIL_ERROR"],
                },
                status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "message": "Success send mail to reset password, check your mail",
                "ticket": ticket,
            }
        )


class ResetPasswordView(APIView):
    def post(self, request, ticket):
        print("reset password ticket: ", ticket)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # new_password=serializer.data['password']
        # print(serializer.data['password'])

        try:
            user_id = take_user_id_from_ticket(ticket)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
        user = UserModel.objects.get(id=user_id)
        newpassword = serializer.data["password"]
        if check_password(newpassword, user.password):
            return Response(
                {
                    "status": False,
                    "message": "Password should not be same with old password",
                    "error_code": ERROR_CODE["OLD_NEW_PASSWORD_NOT_SAME"],
                }
            )

        # oldpassword=OldPasswords.objects.get(user_id=user.id)
        # if check_password(new_password,oldpassword.pwd):
        #     return Response({
        #         'status':False,
        #         "message":"New password....",
        #         'error_code':"4000"
        #     })
        # old_pw=oldpassword.pwd
        # oldpassword.pwd=make_password(old_pw)
        # oldpassword.save()
        # print('user', user.email)

        if user is None:
            return Response(
                {
                    "message": "User doesn't exist",
                    "error_code": ERROR_CODE["USER_NOT_EXIST"],
                }
            )
        print("passowrd: ", user.password)
        user.set_password(serializer.data["password"])
        user.save()
        return Response({"message": "Password reset successfully"})
