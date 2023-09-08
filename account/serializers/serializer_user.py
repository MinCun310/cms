from rest_framework import serializers

from ..models import UserModel
from ..mixin.update import UpdateMixin

class UserSerializer(UpdateMixin, serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('password', 'two_fa_secret')
        allow_update_fields = ['first_name', 'last_name', 'phone']