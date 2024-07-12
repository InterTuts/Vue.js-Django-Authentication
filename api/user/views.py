# System Utils
from django.utils.translation import gettext_lazy as _

# Installed Utils
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# App Utils
from .serializers import UserInfoSerializer 

class UserInfoView(RetrieveAPIView):
    """
    Get the user's information
    """
    # Serializer for user's info
    serializer_class = UserInfoSerializer

    # Authentication class to authenticate the user by token
    authentication_classes = [TokenAuthentication]

    # Class to verify if the user is authenticated
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Returns the authenticated
        user data
        """
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        # Get the user's data
        instance = self.get_object()

        # Serialize the data
        serializer = self.get_serializer(instance)
        
        # Return custom message
        return Response(
            {
                "success": True,
                "content": serializer.data
            },
            status=status.HTTP_200_OK
        )