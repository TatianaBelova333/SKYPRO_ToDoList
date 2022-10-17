from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'password_repeat',
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])

        user.save()
        return user


class CurrentUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'image',
        ]
