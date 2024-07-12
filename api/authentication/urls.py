# System Utils
from django.urls import path

# App Utils
from .views import CreateAccountView, CreateAccountWithGoogleView, SignInAccountView, ResetPasswordView, ChangePasswordView, GoogleConnectView, GoogleCodeView

# Namespace for the auth app
app_name = 'authentication'

urlpatterns = [
    path('registration', CreateAccountView.as_view(), name='registration'),
    path('social-registration', CreateAccountWithGoogleView.as_view(), name='social-registration'),
    path('sign-in', SignInAccountView.as_view(), name='sign-in'),
    path('password-reset', ResetPasswordView.as_view(), name='password-reset'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('google-connect', GoogleConnectView.as_view(), name='google-connect'),
    path('google-code', GoogleCodeView.as_view(), name='google-code'),
]