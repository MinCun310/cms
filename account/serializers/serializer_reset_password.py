from rest_framework import serializers

import re

class SendMailToResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    
    
class ResetPasswordSerializer(serializers.Serializer):
    def validate_password(self, value):
        pat = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$%&*?!])[A-Za-z\d!@$%&*?]{12,25}$")
        if not re.fullmatch(pat, value):
            raise serializers.ValidationError('Password must have atleast one special character, '
                                              'one number, one uppercase, one lowercase '
                                              'and length beetween 12 and 25')
        return value
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("password confirm shouldn't be same")
        return data
    
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    