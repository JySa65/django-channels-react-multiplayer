from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

from app.serializers import UserSerializer, LoginSerializer
from app.models import Winner


class LoginUser(ObtainAuthToken):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data["email"])
            auth_user = authenticate(
                username=user.username, password=request.data["password"]
            )
            token, created = Token.objects.get_or_create(user=auth_user)
            return Response(
                {
                    "token": token.key,
                    "username": auth_user.username,
                    "email": auth_user.email,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response("this user does not exist", status=400)


class GetUser(ObtainAuthToken):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CreateUser(ObtainAuthToken):
    """
    Creates the user.
    """

    def post(self, request, format="json"):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                if user:
                    token = Token.objects.create(user=user)
                    response = serializer.data
                    response["token"] = token.key
                    Winner.objects.create(winner=user)
                    return Response(response, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            raise serializers.ValidationError()
