# System Utils
from django.utils.translation import gettext_lazy as _

# Installed Utils
from rest_framework import serializers

# App Utils
from .models import CustomUser

# Serializer for registration
class UserSerializer(serializers.ModelSerializer):

    # Fields for serialization
    email: str = serializers.EmailField(required=True)
    password: str = serializers.CharField(write_only=True)

    # User's Fields and rules for password
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, email) -> str:
        """
        Validate the email
        """

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('This email address is already registered.'))
        
        if not email.strip():
            raise serializers.ValidationError(_('Email address cannot be blank.'))
        
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError(_('Enter a valid email address.'))

        return email
    
    def validate_password(self, password) -> str:
        """
        Validate the password
        """

        min_length: int = 8
        max_length: int = 20

        if len(password) < min_length or len(password) > max_length:
            raise serializers.ValidationError(_('The password must be between 8 and 20 characters long.'))

        if ' ' in password:
            raise serializers.ValidationError(_('The password cannot contain spaces.'))

        return password

    def create(self, validated_data) -> CustomUser:
        """
        Create the user
        """
        user: CustomUser = CustomUser.objects.create_user(**validated_data)
        return user
    
# Serializer for registration with Google API
class UserSocialRegistrationSerializer(serializers.ModelSerializer):

    # Fields for serialization
    social_id: int = serializers.CharField(max_length=255, required=True)
    email: str = serializers.EmailField(required=True)
    password: str = serializers.CharField(write_only=True)

    # User's Fields and rules for password
    class Meta:
        model = CustomUser
        fields = ['email', 'social_id', 'password']

    def validate_social_id(self, social_id) -> int:
        """
        Validate the social id
        """

        if CustomUser.objects.filter(social_id=social_id).exists():
            raise serializers.ValidationError(_('This social id is already registered.'))

        return social_id

    def validate_email(self, email) -> str:
        """
        Validate the email
        """

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(_('This email address is already registered.'))
        
        if not email.strip():
            raise serializers.ValidationError(_('Email address cannot be blank.'))
        
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError(_('Enter a valid email address.'))

        return email
    
    def validate_password(self, password) -> str:
        """
        Validate the password
        """

        min_length: int = 8
        max_length: int = 20

        if len(password) < min_length or len(password) > max_length:
            raise serializers.ValidationError(_('The password must be between 8 and 20 characters long.'))

        if ' ' in password:
            raise serializers.ValidationError(_('The password cannot contain spaces.'))

        return password

    def create(self, validated_data) -> CustomUser:
        """
        Create the user
        """
        user: CustomUser = CustomUser.objects.create_user(**validated_data)
        return user
    
# Serializer for login
class SignInAccountSerializer(serializers.ModelSerializer):
    
    # Fields for serialization
    email: str = serializers.EmailField()
    password: str = serializers.CharField(max_length=20, write_only=True)

    # Specify the user's fields used for serialization
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

# Serializer for email
class EmailSerializer(serializers.Serializer):

    # Fields for serialization
    email = serializers.EmailField()

# Serializer for password change
class ChangePasswordSerializer(serializers.Serializer):

    # Fields for serialization
    token: str = serializers.CharField(required=True)
    password: str = serializers.CharField(write_only=True)
    
    def validate_password(self, password) -> str:
        """
        Validate the password
        """

        min_length: int = 8
        max_length: int = 20

        if len(password) < min_length or len(password) > max_length:
            raise serializers.ValidationError(_('The password must be between 8 and 20 characters long.'))

        if ' ' in password:
            raise serializers.ValidationError(_('The password cannot contain spaces.'))

        return password
    
# Serializer for authorization code
class AuthorizationCodeSerializer(serializers.Serializer):
    
    # Fields for serialization
    code: str = serializers.CharField(required=True, max_length=250, write_only=True)