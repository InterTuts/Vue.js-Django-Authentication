# System Utils
from django.urls import path

# App Utils
from .views import UserInfoView

# Namespace for the user app
app_name = 'user'

urlpatterns = [
    path('info', UserInfoView.as_view(), name='info')
]