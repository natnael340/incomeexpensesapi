'''
urls file for authentication and authorization
'''

from django.urls import path
from .views import RegisterView, VerifyEmail




urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/<token>', VerifyEmail.as_view(), name='verify_email'),
]
