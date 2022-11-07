from rest_framework import serializers
from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TELEGRAM_BOT_TOKEN


class TgUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        read_only_fields = ("id", "tg_chat_id", "tg_user_id")
        fields = "__all__"

    def validate(self, data: dict):
        verification_code = data.get('verification_code')
        tg_user = TgUser.objects.filter(verification_code=verification_code)
        if not tg_user:
            raise serializers.ValidationError("Incorrect verification code")
        return data

    def update(self, instance, validated_data):
        tg_user = TgUser.objects.get(verification_code=validated_data['verification_code'])
        tg_user.is_verified = True
        tg_user.user = self.context['request'].user
        tg_user.save()
        tg_client = TgClient(token=TELEGRAM_BOT_TOKEN, tg_user=TgUser)
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text='Verification completed')
        return tg_user
