from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Welcome to EthioFlavor API!",
        "endpoints": {
            "recipes": "/api/recipes/",
            "register": "/api/auth/register/", 
            "login": "/api/auth/login/",
            "admin": "/admin/"
        },
        "description": "A RESTful API for managing Ethiopian recipes."
    })