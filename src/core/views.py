from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSignUpSerializer, UserLoginSerializer, UserProfileSerializer, PasswordUpdateSerializer


class SignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer


class LoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


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
    serializer_class = PasswordUpdateSerializer

    def get_object(self) -> User:
        return self.request.user
