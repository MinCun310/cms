from django.core.cache import cache

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers import LoginSerializer,DeviceSerializer

from ..libs.device import store_device
from ..libs.otp import generate_otp_code
from ..libs.mail import send_mail_with_otp
from ..libs.ticket import generate_ticket

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
        
        device = store_device(request, user)
        # print('device_info', device)
        ticket = generate_ticket(user, device)
        print('---------------------')
        print('ticket: ', ticket)
        code = generate_otp_code()
        print('---------------------')
        print('code: ', code)
        
        if send_mail_with_otp(code, user.email):
            # save ticket in cache
            cache.set(ticket, code, timeout=60)
            return Response({
                'message': 'Email verify required',
                'ticket': ticket
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': True,
                'error_message': 'Error sending OTP',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({
        #     "data": {
        #         "data": serializer.data,
        #     }
        # })
        