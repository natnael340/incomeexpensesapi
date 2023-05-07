'''
urls file for authentication and authorization
'''

from django.urls import path
from .views import RegisterView, VerifyEmail, LoginApiView, RequestPasswordResetEmail, PasswordResetTokenCheckView, ResetPasswordApiView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/<token>', VerifyEmail.as_view(), name='verify_email'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('password-reset-request', RequestPasswordResetEmail.as_view(), name='password_reset_request'),
    path('password-reset-check/<uidb64>/<token>', PasswordResetTokenCheckView.as_view(), name='password_reset_check'),
    path('password-reset', ResetPasswordApiView.as_view(), name='password_reset'),
]
