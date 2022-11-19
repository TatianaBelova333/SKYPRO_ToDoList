from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from bot.models import TgUser
from bot.serializers import TgUserSerializer


class BotVerificationView(UpdateAPIView):
    """Verify the web application user's account with the verification code sent by telegram bot."""

    queryset = TgUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def get_object(self):
        return self.request.user
