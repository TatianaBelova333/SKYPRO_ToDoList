from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import UserSignUpSerializer, UserLoginSerializer, UserProfileSerializer, PasswordUpdateSerializer


class SignUpView(CreateAPIView):
    """Register a new user"""
    serializer_class = UserSignUpSerializer


class LoginView(CreateAPIView):
    """Log in an existing user with username and password"""
    serializer_class = UserLoginSerializer

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


class ProfileView(RetrieveUpdateDestroyAPIView):
    """Show logged-in user's profile"""
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self) -> User:
        """Return current user"""
        return self.request.user

    def delete(self, request, *args, **kwargs):
        """Log out the logged-in user"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateView(UpdateAPIView):
    """Update user's current password"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PasswordUpdateSerializer

    def get_object(self) -> User:
        return self.request.user
