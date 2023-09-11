from rest_framework import serializers
from ..models import UserModel
import re

class LoginSerializer(serializers.Serializer):
    # def validate_email(self, value):
    #     pat = re.compile(r"^\S+@\S+$")
    #     if not re.fullmatch(pat, value):
    #         raise serializers.ValidationError("Email is not valid")
    #     return value
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=200, write_only=True)
    