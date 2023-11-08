from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    def validate_new_password(self, value):
        validate_password(value)
        return value

    old_password = serializers.CharField()
    new_password = serializers.CharField()
