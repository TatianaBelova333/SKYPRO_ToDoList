from django.contrib import admin

from bot.models import TgUser


class TgBotAdmin(admin.ModelAdmin):
    list_display = ("id", "tg_chat_id", "tg_user_id", "user", "verification_code", "is_verified")
    search_fields = ("user",)


admin.site.register(TgUser, TgBotAdmin)
