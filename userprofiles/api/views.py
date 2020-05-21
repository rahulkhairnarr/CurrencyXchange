from django.contrib.auth import get_user_model
from userprofiles.api.serializers import UserSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from userprofiles.models import Profile
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate



@api_view(['POST',])
def create_user(request):
    user = User()
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {"token": token.key}
        print(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def login_user(request):
    username = authenticate(username=request.data['username'], password=request.data['password'])
    print(username)
    if username is not None:
        user = User.objects.get(username = username)
        serializer = UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        data = {"token": token.key}
        return Response(data, status=status.HTTP_200_OK)
    else:
        data = {"message" : "Invalid Credentials"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['PUT',])
def upload_photo(request):
    user = request.user
    try:
        profile, create = Profile.objects.get_or_create(user=user)
    except Profile.DoesNotExist as e:
        return Response({"message": "User Profile Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)