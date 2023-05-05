from django.shortcuts import render
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
# Create your views here.

class RegisterView(generics.GenericAPIView):
    """
    
    This view is used to register a new user

    params:
     - username: a unique username and it must be alphanumeric
     - email: a unique and valid email address
     - password: a password it must be greater than 8 and less than 128

    Up on successful registration of the user, the endpoints will sent
    email verification toke which is a jwt token containing the user id
    """
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer, )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        verify_link = f'http://{get_current_site(request=request).domain}{reverse("verify_email", kwargs={"token": token})}'
        email_body = f'Hi, {user.username} \n Use the following link to verify your email \n {verify_link}'
        data = {
            'email_body': email_body,
            'email_subject': 'Verify your email',
            'email_to': user.email
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer  
    '''
    This is an enpoint that allows user to verify their email

    params:
     - token

    Given a valid token, it extracts the user id from the token and
    change is_verified attribute of the user
    '''
    token_param_config = openapi.Parameter('token', in_=openapi.IN_PATH, description='verfiying email using email verfication token', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, token):
       
        try:           
            payload = jwt.decode(str(token).encode(), settings.SECRET_KEY, ['HS256'])
    
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'success': True, 'message': 'Email successfully verified'}, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError as identifier:
            return Response({'success': False, 'message': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'success': False, 'message': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
