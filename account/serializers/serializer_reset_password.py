from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
import re
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User =get_user_model()
class SendMailToResetPasswordSerializer(serializers.Serializer):
    def validate_email(self,value):
        try:  
            User.objects.get(email=value)
        except Exception:
            raise serializers.ValidationError("User doesn't exists")
        return value
    email = serializers.CharField()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    def validate_password(self, value):
    #     pat = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$%&*?!])[A-Za-z\d!@$%&*?]{12,25}$")
    #     if not re.fullmatch(pat, value):
    #         raise serializers.ValidationError('Password must have atleast one special character, '
    #                                           'one number, one uppercase, one lowercase '
    #                                           'and length beetween 12 and 25')
    #     return value
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError("password confirm shouldn't be same")
    #   return data
    
        validate_password(value)
        return value

    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    