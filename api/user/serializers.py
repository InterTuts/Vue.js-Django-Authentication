# Installed Utils
from rest_framework import serializers

# App Utils
from authentication.models import CustomUser

# Serializer for user data reading
class UserInfoSerializer(serializers.ModelSerializer):
    """
    Is used to specify which
    user fields should be read
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email']