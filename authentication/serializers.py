from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        #check if email contains only alphanumeric characters
        if not username.isalnum(): 
            raise serializers.ValidationError('Username should only contain alphanumeric characters')
        
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=512)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=128, min_length=5)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    username = serializers.CharField(max_length=128, min_length=8, read_only=True)
    refresh_token = serializers.CharField(max_length=256, min_length=8, read_only=True)
    access_token = serializers.CharField(max_length=256, min_length=8, read_only=True)


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials, please try again')
        elif not user.is_active:
            raise AuthenticationFailed('Account blocked, Contact admin')
        elif not user.is_verified:
            raise AuthenticationFailed('Email not verified, please verify your email address')
        
        tokens = user.tokens()
        return {
            'email': user.email,
            'username': user.username,
            'refresh_token': tokens['refresh'],
            'access_token': tokens['access']
        }

       