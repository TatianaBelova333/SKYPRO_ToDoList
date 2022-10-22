from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSignUpSerializer, UserLoginSerializer, UserProfileSerializer


class SignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer


class LoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())
"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login(request=request, user=serializer.save())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self) -> User:
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self) -> User:
        return self.request.user

