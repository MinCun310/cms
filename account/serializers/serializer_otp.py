from rest_framework import serializers
from ..models import UserModel


class OTPVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=9)
    ticket = serializers.CharField(max_length=255)


class OTPRefreshSerializer(serializers.Serializer):
    ticket = serializers.CharField(max_length=255)
