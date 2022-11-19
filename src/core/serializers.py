from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from core.models import User


class PasswordField(serializers.CharField):
    """Password field serializer class."""

    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""

    password = PasswordField()
    password_repeat = PasswordField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        ]

    def validate(self, data: dict) -> dict:
        """Validate if raw password and password_repeat match."""
        if data['password'] != data['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match.'})
        return data

    def create(self, validated_data: dict) -> User:
        """Create a new User instance hashing the password."""
        del validated_data['password_repeat']
        password = validated_data['password']

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer for logging in the user."""

    username = serializers.CharField()
    password = PasswordField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data: dict) -> User:
        """Authenticate and log in the user."""
        user = authenticate(
            username=validated_data['username'],
            password=validated_data["password"],
        )
        if not user:
            raise AuthenticationFailed
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the current user profile."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PasswordUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating the current user's password."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField()
    new_password = PasswordField()

    class Meta:
        model = User
        fields = ['user', 'old_password', 'new_password']

    def validate(self, data: dict) -> dict:
        """Validate old password field against user's database current password"""
        user = data['user']
        old_password = data['old_password']
        new_password = data['new_password']

        if not user:
            raise NotAuthenticated
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'Old password is incorrect'})
        if old_password == new_password:
            raise ValidationError({'new_password': 'New password must differ from the old password'})
        return data

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, user: User, validated_data: dict) -> User:
        """Update and hash the current user's password."""
        new_password = validated_data['new_password']
        user.set_password(new_password)
        user.save(update_fields=('password',))
        return user
