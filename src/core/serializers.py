from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated

from core.models import User


class PasswordField(serializers.CharField):

    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserSignUpSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

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

    def validate(self, attrs: dict):
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('The passwords do not match')
        return attrs

    def create(self, validated_data: dict):
        del validated_data['password_repeat']
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)


    class Meta:
        model = User
        fields = ['username', 'passwords']

    def create(self, validated_data: dict):
        user = authenticate(
            username=validated_data['username'],
            password=validated_data["password"]
        )
        if not user:
            raise AuthenticationFailed
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class UpdatePasswordSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(read_only=True)
    new_passwowrd = PasswordField(read_only=True)

    def validate(self, attrs: dict):
        user = attrs['user']
        if not user:
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise ValidationError('Old password is incorrect')
        return attrs

    def create(self, validated_data: dict):
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict):
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance

