from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "Welcome to EthioFlavor API!",
        "endpoints": {
            "recipes": "/api/recipes/",
            "categories": "/api/recipes/categories/",
            "ingredients": "/api/recipes/ingredients/",
            "cultural-tags": "/api/recipes/cultural-tags/",
            "register": "/api/auth/register/", 
            "login": "/api/token/",
            "token_refresh": "/api/token/refresh/",
            "users": "/api/users/",
            "admin": "/admin/"
        },
        "description": "A RESTful API for managing Ethiopian recipes with authentication and advanced features."
    })