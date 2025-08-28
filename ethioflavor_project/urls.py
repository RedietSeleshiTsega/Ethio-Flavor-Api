from django.contrib import admin
from django.urls import path, include 
from rest_framework.authtoken.views import obtain_auth_token
from users.views import RegisterView
from api.views import api_home

urlpatterns = [
    path('', api_home, name='home'),
    path('admin/', admin.site.urls),
    path('api/recipes/', include('recipes.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', obtain_auth_token, name='login'),
]