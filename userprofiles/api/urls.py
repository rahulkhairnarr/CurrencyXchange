from userprofiles.api.views import create_user, login_user, upload_photo
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users_api'

urlpatterns = [
    path('registration/',create_user, name='registration'),
    path('login/',login_user, name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('upload_photo/',upload_photo, name='upload_photo'),
]
