from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from bot.models import TgUser
from bot.serializers import TgUserSerializer


class BotVerificationView(UpdateAPIView):
    queryset = TgUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def get_object(self):
        return self.request.user
