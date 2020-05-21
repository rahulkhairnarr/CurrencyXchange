from rest_framework import serializers
from django.contrib.auth import get_user_model
from userprofiles.models import Profile

# from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  get_user_model()

        fields = ['username','password']
        extra_kwargs = {'password': {'write_only': True}}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Profile

        fields = ['profile_img']