from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import UserModel

from ..serializers import RegisterSerializer
from ..serializers import DeviceSerializer
from ..libs.device import store_device

class RegisterView(APIView):
    
    def post(self, request):
        print(request.data)
        # request.data là data truyền từ client về vd: dùng postman (POST) giả lập data truyền từ client về
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "Message":"invalid data",
                "Error_fields": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        
        return Response({
            "message":"Registered successfully",
            "data": {
                "user": serializer.data,
            }
        })
        