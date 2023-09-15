from rest_framework import serializers
from ..models import UserModel

class MyAcccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('name', 'email', 'phone', 'address', 'country', 'state/region', 'city', 'zip/code', 'about')