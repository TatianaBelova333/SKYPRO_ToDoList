from django.urls import path

from bot.views import BotVerificationView


app_name = 'bot'


urlpatterns = [
     path("verify", BotVerificationView.as_view(), name='verify_bot'),

]
