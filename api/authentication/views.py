# System Utils
import requests
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views import View
from urllib.parse import urlencode

# Installed Utils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django_ratelimit.decorators import ratelimit
from django_rest_passwordreset.models import ResetPasswordToken, clear_expired

# App Utils
from .models import CustomUser
from .serializers import UserSerializer, UserSocialRegistrationSerializer, SignInAccountSerializer, EmailSerializer, ChangePasswordSerializer, AuthorizationCodeSerializer
from .permissions import IsNotAuthenticated

HTTP_USER_AGENT_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(settings, 'DJANGO_REST_PASSWORDRESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')

# Create Account
class CreateAccountView(CreateAPIView):
    queryset = None
    serializer_class = UserSerializer
    permission_classes = [IsNotAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request):
        # Get information about serialization
        serializer = self.get_serializer(data=request.data)

        # Check if the received data is correct
        if not serializer.is_valid():

            # Default error message
            errorMsg: str = _('An error has occurred.')

            # Check if the error is for email
            if ( serializer.errors.get('email') != None ):
                errorMsg = serializer.errors['email'][0].capitalize()
            elif ( serializer.errors.get('password') != None ):
                errorMsg = serializer.errors['password'][0].capitalize()

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": errorMsg
                },
                status=status.HTTP_200_OK
            )

        # Try to create the user
        try:
            serializer.save()
        except Exception as e:
            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('An unknown error occurred.')
                },
                status=status.HTTP_200_OK
            )             

        # Return custom message
        return Response(
            {
                "success": True,
                "message": _('The account was created successfully.')
            },
            status=status.HTTP_201_CREATED
        )
    
# Create Account using Google API
class CreateAccountWithGoogleView(CreateAPIView):
    queryset = None
    serializer_class = UserSocialRegistrationSerializer
    permission_classes = [IsNotAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request):
        # Get information about serialization
        serializer = self.get_serializer(data=request.data)

        # Check if the received data is correct
        if not serializer.is_valid():

            # Default error message
            errorMsg: str = _('An error has occurred.')

            # Check if the error is for email
            if ( serializer.errors.get('email') != None ):
                errorMsg = serializer.errors['email'][0].capitalize()
            elif ( serializer.errors.get('social_id') != None ):
                errorMsg = serializer.errors['social_id'][0].capitalize()
            elif ( serializer.errors.get('password') != None ):
                errorMsg = serializer.errors['password'][0].capitalize()

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": errorMsg
                },
                status=status.HTTP_200_OK
            )

        # Try to create the user
        try:
            serializer.save()
        except Exception:
            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('An unknown error occurred.')
                },
                status=status.HTTP_200_OK
            )             

        # Return custom message
        return Response(
            {
                "success": True,
                "message": _('The account was created successfully.')
            },
            status=status.HTTP_201_CREATED
        )
    
# Sign In
class SignInAccountView(APIView):
    permission_classes = [IsNotAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request):
        # Get information about serialization
        serializer = SignInAccountSerializer(data=request.data)

        # Check if the received data is correct
        if not serializer.is_valid():

            # Default error message
            errorMsg: str = _('An error has occurred.')

            # Check if the error is for email
            if ( serializer.errors.get('email') != None ):
                errorMsg = serializer.errors['email'][0].capitalize()
            elif ( serializer.errors.get('password') != None ):
                errorMsg = serializer.errors['password'][0].capitalize()

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": errorMsg
                },
                status=status.HTTP_200_OK
            )

        # Get email
        email = serializer.validated_data.get('email')

        # Get password
        password = serializer.validated_data.get('password')

        # Lets login
        user = authenticate(email=email, password=password)

        # Check if login is successfully
        if user:
            # Delete existing token if it exists
            Token.objects.filter(user=user).delete()

            # Create a new token
            token = Token.objects.create(user=user)

            # Return custom message
            return Response(
                {
                    "success": True,
                    "message": _('You have successfully signed in.'),
                    "content": {
                        "id": user.id,
                        "email": user.email,
                        "token": token.key
                    }
                },
                status=status.HTTP_200_OK
            )

        else:

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('The email or password is not correct.')
                },
                status=status.HTTP_200_OK
            )
        
class ResetPasswordView(RetrieveAPIView):
    serializer_class = EmailSerializer
    
    def post(self, request, *args, **kwargs):
        # Get information about serialization
        serializer = self.get_serializer(data=request.data)

        # Check if the received data is correct
        if not serializer.is_valid():

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('The e-mail is not valid.')
                },
                status=status.HTTP_200_OK
            )
            
        try:

            # Get email
            email = serializer.validated_data.get('email')

            # Get user's data
            user = CustomUser.objects.get(email=email)

            # datetime.now minus expiry hours
            now_minus_expiry_time = timezone.now() - timedelta(minutes=15)

            # delete all tokens where created_at < now - 15 minutes
            clear_expired(now_minus_expiry_time)

            # Generate a reset token
            token = ResetPasswordToken.objects.create(
                user=user,
                user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
            )

            # Get the email template
            email_html_message = render_to_string('email/user_reset_password.html', {
                'reset_password_url': "{}/{}".format(
                    request.build_absolute_uri(settings.WEBSITE_URL + 'change-password'),
                    token.key)
            })

            # Prepare the email data
            msg = EmailMultiAlternatives(
                # Title:
                _('Password Reset'),
                # Message:
                email_html_message,
                # From:
                settings.EMAIL_SENDER,
                # To:
                [email]
            )

            # Send email with html code
            msg.attach_alternative(email_html_message, "text/html")
        
            # Send email
            num_sent_emails = msg.send()

            # Check if email was sent
            if num_sent_emails == 1:
                # Return custom message
                return Response(
                    {
                        "success": True,
                        "message": _('The password reset e-mail has been sent.')
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": _('The password reset was not sent successfully.')
                    },
                    status=status.HTTP_200_OK
                )
        
        except CustomUser.DoesNotExist:
            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('The e-mail not associated to any user.')
                },
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('An unknown error occurred.')
                },
                status=status.HTTP_200_OK
            ) 
        

class ChangePasswordView(APIView):
    permission_classes = [IsNotAuthenticated]

    def put(self, request):

        # Serialize data
        serializer = ChangePasswordSerializer(data=request.data)

        # Check if the data is not valid
        if not serializer.is_valid():
            # Default error message
            errorMsg: str = _('An error has occurred.')

            # Check if the error is for password
            if ( serializer.errors.get('password') != None ):
                errorMsg = serializer.errors['password'][0].capitalize()

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": errorMsg
                },
                status=status.HTTP_200_OK
            )
        
        # Get the token
        token = serializer.validated_data.get('token')

        # Get the password
        password = serializer.validated_data.get('password')

        try:

            # Get token's information
            reset_password_token = ResetPasswordToken.objects.get(key=token)
            
            # Calculate the expiration time
            expiration_time = reset_password_token.created_at + timezone.timedelta(minutes=15)

            # Check if the token is expired
            if timezone.now() > expiration_time:
                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": _('The confirmation token is expired.')
                    },
                    status=status.HTTP_200_OK
                )                 
            
            # Get user's data
            user = reset_password_token.user

            # Set new password
            user.set_password(password)

            # Save password
            user.save()

            # Return custom message
            return Response(
                {
                    "success": True,
                    "message": _('The password was changed successfully.')
                },
                status=status.HTTP_200_OK
            )

        except ResetPasswordToken.DoesNotExist:

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('The confirmation token is not valid.')
                },
                status=status.HTTP_200_OK
            )            

        except Exception:

            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('An unknown error occurred.')
                },
                status=status.HTTP_200_OK
            )
        
class GoogleConnectView(View):
    def get(self, request):
        # Login params
        auth_params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
            'redirect_uri': settings.WEBSITE_URL + 'api/google/connect',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }

        # Build the login URL
        login_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"

        # Redirect to Google
        return redirect(login_url)

class GoogleCodeView(APIView):
    permission_classes = [IsNotAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='3/m', block=True))
    def post(self, request, *args, **kwargs):

        # Get information about serialization
        serializer = AuthorizationCodeSerializer(data=request.data)

        # Check if the received data is correct
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": _('The authorization code is not valid.')
                },
                status=status.HTTP_200_OK
            )
        
        # Try to create the user
        try:
            # Get the authorization code
            code = serializer.validated_data.get('code')

            # Create the content for the POST request
            content = {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'code': code,
                'redirect_uri': settings.WEBSITE_URL + 'api/google/connect',
                'grant_type': 'authorization_code',
                'access_type': 'offline',
                'prompt': 'consent'
            }

            # Request the access token
            token_request = requests.post('https://www.googleapis.com/oauth2/v4/token', data=content)

            # Parse the json content
            json_response = token_request.json()

            # Check if the request was successful
            if token_request.status_code != 200:

                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": json_response.get('error_description', 'An error occurred')
                    },
                    status=status.HTTP_200_OK
                )

            # Extract the access token
            access_token = json_response.get('access_token')

            # Verify if access token is missing
            if not access_token:
                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": _('Access token not found in the response.')
                    },
                    status=status.HTTP_200_OK
                )

            # Initialize a new HttpClient session
            account_data_response = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}')

            # Parse the json content
            user_info = account_data_response.json()

            # Extract the user's id
            social_id = user_info.get('id')

            # Verify if user id is missing
            if not social_id:
                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": _('User id not found in the response.')
                    },
                    status=status.HTTP_200_OK
                )
            
            # Get the user by social id
            user = CustomUser.objects.filter(social_id=social_id).first()

            # Verify if user exists
            if ( user ):

                # Delete existing token if it exists
                Token.objects.filter(user=user).delete()

                # Create a new token
                token = Token.objects.create(user=user)

                # Return custom message
                return Response(
                    {
                        "success": True,
                        "message": _('You have successfully signed in.'),
                        "content": {
                            "id": user.id,
                            "email": user.email,
                            "token": token.key
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            
            # Extract the user's email
            email = user_info.get('email')

            # Verify if user email is missing
            if not email:
                # Return custom message
                return Response(
                    {
                        "success": False,
                        "message": _('User email not found in the response.')
                    },
                    status=status.HTTP_200_OK
                )

            # Return custom message
            return Response(
                {
                    "success": True,
                    "content": {
                        "social_id": social_id,
                        "email": email
                    }
                },
                status=status.HTTP_200_OK
            )
        
        except Exception:
            # Return custom message
            return Response(
                {
                    "success": False,
                    "message": _('An unknown error occurred.')
                },
                status=status.HTTP_200_OK
            ) 