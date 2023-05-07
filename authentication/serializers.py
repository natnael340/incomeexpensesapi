from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

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

       
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=6)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
          
            current_site = get_current_site(self.context.get('request')).domain
            relativeUrl = reverse('password_reset_check', kwargs={'token': token, 'uidb64': uidb64})
            absoluteUrl = f'http://{current_site}/{relativeUrl}'.format(current_site, relativeUrl)
            email_body  = f"Hello, \n Here is your password reset url {absoluteUrl}".format(url=absoluteUrl)
            data = {"email_body": email_body, 'email_to': user.email, 'email_subject': 'Reset Password'}
                
            Util.send_email(data)
        else:
            raise serializers.ValidationError('User does not exist')
        return super().validate(attrs)
    
class PasswordResetTokenCheckSerializer(serializers.Serializer):
    pass

class ResetPassword(serializers.Serializer):
    """Serializer for setting new password given the token and uuid."""
    password = serializers.CharField(required=True, write_only=True)
    uidb64 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs:dict):
        """Validate uidb64, token, and the new password to update the users password."""
        try:
            uid = smart_str(urlsafe_base64_decode(attrs.get('uidb64', '')))
            
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user, attrs.get('token')):
                raise AuthenticationFailed('The reset token is invalid', "401")
            user.set_password(attrs.get('password'))
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset token is invalid', "401")
        return super().validate(attrs)
