# System Utils
from django.utils.translation import gettext_lazy as _

# Installed Utils
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom the exceptions
    messages
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status_code'] = response.status_code
        
    if hasattr(exc, 'detail'):
        return Response(
            {
                "success": False,
                "message": exc.detail
            },
            status=status.HTTP_200_OK
        )      
    elif exc != None:
        return Response(
            {
                "success": False,
                "message": exc
            },
            status=status.HTTP_200_OK
        )    
    else:
        return Response(
            {
                "success": False,
                "message": _('An unknown error occurred.')
            },
            status=status.HTTP_200_OK
        )