from rest_framework import serializers
from ..models import UserModel
from django.contrib.auth import get_user_model

User = get_user_model


class MyAcccountInfoSerializer(serializers.ModelSerializer):
    zip_code = serializers.CharField(max_length=5)
    avatar_url = serializers.ReadOnlyField()

    def validate_email(self, value):
        # self.instance lấy user hiện tại
        old_user = self.instance
        is_exists = UserModel.objects.filter(email=value).exists()
        print(10, is_exists)
        print("old_user: ", old_user.email)
        print(value)
        if old_user.email != value and is_exists:
            raise serializers.ValidationError("Email is existed")
        return value

    class Meta:
        model = UserModel
        fields = (
            "id",
            "avatar_url",
            "name",
            "email",
            "phone",
            "address",
            "country",
            "zip_code",
            "state/region",
            "city",
            "about",
            "username",
        )

    def update(self, instance, validated_data):
        old_email = instance.email
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if "email" in validated_data and old_email != validated_data["email"]:
            instance.username = validated_data["email"].split("@")[0]
        instance.save()
        return instance
