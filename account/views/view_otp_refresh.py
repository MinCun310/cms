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
from smtplib import SMTPException
from django.core.cache import cache

class OTPRefreshView(APIView):
    permission_classes = [AllowAny, ]
    
    def post(self, request):
        serializer = OTPRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        
        timeout = cache.ttl(data["ticket"])
        user_id = take_user_id_from_ticket(data["ticket"])
        user = UserModel.objects.get(id=user_id)

        # if timeout != 0:
        #     return Response({
        #         "ticket": data["ticket"],
        #         "timeout": timeout
        #     }, status.HTTP_400_BAD_REQUEST)
            
        device = store_device(request, user)
        ticket = generate_ticket(user, device)
        code = generate_otp_code()
        print("resend code: ", code)
        try:  
            send_mail_with_otp(code, user.email)
            cache.set(ticket, code, timeout=60)
        except SMTPException:
             return Response({
                'message': 'Error sending OTP',
            }, status.HTTP_400_BAD_REQUEST)
        return Response({
                'has_otp': True,
                'ticket': ticket
            })
           
        