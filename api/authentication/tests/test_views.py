# System Utils
from django.http import HttpResponse
from django.urls import reverse

# Installed Utils
from rest_framework import status
from rest_framework.authtoken.models import Token
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework.test import APITestCase, APIClient

# App Utils
from authentication.models import CustomUser

"""
TEST EMAIL REGISTRATION
"""

class CreateAccountViewTest(APITestCase):
    """
    This class is used to test
    the user registration
    """

    def setUp(self) -> None:

        # Api Client to simulate http requests
        self.client = APIClient()

        # Define the URL for the CreateAccountView
        self.url = reverse('authentication:registration')     

    def test_create_valid_user(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser@example.com',
            'password': 'newpassword'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check for success response
        self.assertTrue(response.data['success'])

        # Verify if there are 1 users
        self.assertEqual(CustomUser.objects.count(), 1)

        # Get the last user data
        second_user: CustomUser = CustomUser.objects.last()

        # Check if email is equal 
        self.assertEqual(second_user.email, 'existinguser@example.com')

    def test_create_user_short_password(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser@example.com',
            'password': 'new'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The password must be between 8 and 20 characters long.')

        # Verify if there are 0 users
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_create_user_invalid_email(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser',
            'password': 'newpassword'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'Enter a valid email address.')

        # Verify if there are 0 users
        self.assertEqual(CustomUser.objects.count(), 0)

"""
TEST SOCIAL REGISTRATION
"""

class CreateAccountWithGoogleViewTest(APITestCase):
    """
    This class is used to test
    the user registration with Google
    """

    def setUp(self) -> None:

        # Api Client to simulate http requests
        self.client = APIClient()

        # Define the URL for the CreateAccountWithGoogleView
        self.url = reverse('authentication:social-registration')     

    def test_create_valid_user(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser@example.com',
            'social_id': 1,
            'password': 'newpassword'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check for success response
        self.assertTrue(response.data['success'])

        # Verify if there are 1 users
        self.assertEqual(CustomUser.objects.count(), 1)

        # Get the last user data
        second_user: CustomUser = CustomUser.objects.last()

        # Check if email is equal 
        self.assertEqual(second_user.email, 'existinguser@example.com')

    def test_create_user_short_password(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser@example.com',
            'social_id': 1,
            'password': 'new'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The password must be between 8 and 20 characters long.')

        # Verify if there are 0 users
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_create_user_invalid_email(self) -> None:

        # Prepare user's data
        data: dict[str, str] = {
            'email': 'existinguser',
            'social_id': 1,
            'password': 'newpassword'
        }
        
        # Send post request to create the user
        response: HttpResponse = self.client.post(self.url, data)

        # Compare the status code to see if is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'Enter a valid email address.')

        # Verify if there are 0 users
        self.assertEqual(CustomUser.objects.count(), 0)

"""
TEST EMAIL LOGIN
"""

class SignInAccountViewTest(APITestCase):
    """
    This class is used to test
    the login with email
    """
    
    @classmethod
    def setUpTestData(cls) -> None:
        
        # Create a test user
        cls.user1 = CustomUser.objects.create_user(
            email='info@example.com',
            password='12345678'
        )

    def setUp(self) -> None:
        
        # Api Client to simulate http requests
        self.client = APIClient()

        # Define the URL for the SignInAccountView
        self.url = reverse('authentication:sign-in')

    def test_success_sign_in(self) -> None:

        # Prepare the login data
        login_data: dict[str, str] = {
            'email': 'info@example.com',
            'password': '12345678'
        }

        # Send the login request
        response: HttpResponse = self.client.post(self.url, login_data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for success response
        self.assertTrue(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'You have successfully signed in.')

    def test_sign_in_with_invalid_email(self) -> None:

        # Prepare the login data
        login_data: dict[str, str] = {
            'email': 'example.com',
            'password': '12345678'
        }

        # Send the login request
        response: HttpResponse = self.client.post(self.url, login_data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'Enter a valid email address.')

    def test_sign_in_with_invalid_password(self) -> None:

        # Prepare the login data
        login_data: dict[str, str] = {
            'email': 'info@example.com',
            'password': '12345'
        }

        # Send the login request
        response: HttpResponse = self.client.post(self.url, login_data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The email or password is not correct.')


"""
TEST PASSWORD RESET
"""

class ResetPasswordViewTest(APITestCase):
    """
    This class is used to test
    the reset password link request
    """

    @classmethod
    def setUpTestData(cls) -> None:

        # Create a test user
        cls.user1 = CustomUser.objects.create_user(
            email='info@example.com',
            password='12345678'
        )

    def setUp(self) -> None:

        # Api Client to simulate http requests
        self.client = APIClient()

        # Define the URL for the ResetPasswordView
        self.url = reverse('authentication:password-reset')

    def test_password_reset_request(self) -> None:

        # Prepare the email data
        data: dict[str, str] = {
            'email': 'info@example.com'
        }

        # Send password reset
        response: HttpResponse = self.client.post(self.url, data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for success response
        self.assertTrue(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The password reset e-mail has been sent.')

    def test_password_reset_request_with_wrong_email(self) -> None:

        # Prepare the email data
        data: dict[str, str] = {
            'email': 'contact@example.com'
        }

        # Send password reset
        response: HttpResponse = self.client.post(self.url, data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The e-mail not associated to any user.')


class ChangePasswordViewTest(APITestCase):
    """
    This class is used to test
    the password change request
    """

    def setUp(self) -> None:

        # Api Client to simulate http requests
        self.client = APIClient()

        # Define the URL for the ChangePasswordView
        self.url = reverse('authentication:change-password')

        # Create a test user
        self.user = CustomUser.objects.create_user(
            email='info@example.com',
            password='12345678'
        )

        # Generate an reset password token
        self.token = ResetPasswordToken.objects.create(user=self.user)

    def test_password_change_request(self) -> None:

        # Prepare the email data
        data: dict[str, str] = {
            'token': self.token.key,
            'password': 'newpassword'
        }

        # Send password reset
        response: HttpResponse = self.client.put(self.url, data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for success response
        self.assertTrue(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The password was changed successfully.')

    def test_password_change_request_with_short_password(self) -> None:

        # Prepare the email data
        data: dict[str, str] = {
            'token': self.token.key,
            'password': 'new'
        }

        # Send password reset
        response: HttpResponse = self.client.put(self.url, data)

        # Check for correct status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for failed response
        self.assertFalse(response.data['success'])

        # Verify if the returned message is correct
        self.assertEqual(response.data['message'], 'The password must be between 8 and 20 characters long.')