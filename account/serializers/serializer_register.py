from rest_framework import serializers
from ..models import UserModel
import re

class RegisterSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        pat = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,25}$")
        if not re.fullmatch(pat, value):
            raise serializers.ValidationError("Password must have atleast one special character, one number, one uppercase, one lowercase and length between 12 and 25")
        return value
    
    def validate(self, data):
        # print('data_________')
        # print(data)
        if data['email'] == "data['password']":
            raise serializers.ValidationError("email and password shouldn't be same.")
        return data
    
    class Meta:
        model = UserModel
        fields = ('first_name','last_name','email','password','phone')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }
    
    def create(self, validated_data):
        user = UserModel(**validated_data)
        print(38, validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    