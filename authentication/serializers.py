from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'task_type_preferences', 'friends')
        extra_kwargs = {'password': {'write_only': True}}
        
        def create(self, validated_data):
            password = validated_data.pop('password')
            user = CustomUser(**validated_data)
            if password:
                user.set_password(password)
            user.save()
            return user 
        
        def update(self, user, validated_data):
            for attr, value in validated_data.items():
                if attr == 'password':
                    user.set_password(value)
                else:
                    setattr(user, attr, value)
            user.save()
            return user 
        