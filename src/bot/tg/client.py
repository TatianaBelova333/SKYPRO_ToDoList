from random import sample
from string import hexdigits

import requests

from bot.models import TgUser
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
import marshmallow_dataclass

from goals.models import Goal, Status, GoalCategory


class TgClient:
    def __init__(self, token, tg_user: TgUser):
        self.token = token
        self.tg_user = tg_user

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}?"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates') + f'timeout={timeout}&offset={offset}'
        res = requests.get(url).json()
        res_schema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        return res_schema().load(res)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('sendMessage') + f'chat_id={chat_id}&text={text}'
        res = requests.get(url).json()
        res_schema = marshmallow_dataclass.class_schema(SendMessageResponse)
        return res_schema().load(res)

    @staticmethod
    def generate_verification_code():
        return ''.join(sample(hexdigits, 6))

    def send_verification_code(self, chat_id: int, verification_code: str):
        text = f'Hello! Please verify your account with this code {verification_code}'
        return self.send_message(chat_id, text)

    def tg_user_exists(self, tg_user_id: int) -> bool:
        return self.tg_user.objects.filter(tg_user_id=tg_user_id).exists()

    def tg_user_verified(self, tg_user_id: int) -> bool:
        if self.tg_user_exists(tg_user_id):
            return self.tg_user.objects.get(tg_user_id=tg_user_id).is_verified
        return False

    def create_new_tg_user(self, tg_user_id, chat_id, verification_code):
        self.tg_user.objects.create(
            tg_user_id=tg_user_id,
            tg_chat_id=chat_id,
            verification_code=verification_code
        )

    def update_tg_user(self, tg_user_id, verification_code):
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        tg_user.verification_code = verification_code
        tg_user.save()

    def send_user_goals(self, tg_user_id, chat_id):
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user.id
        ).exclude(status=Status.archived)
        if goals:
            text = '\n'.join(goal.title for goal in goals)
        else:
            text = "You don't have any planned goals."
        return self.send_message(text=text, chat_id=chat_id)

    def send_user_categories(self, tg_user_id, chat_id):
        categories = self.get_user_categories(tg_user_id)
        if categories:
            categories_list = '\n'.join(categories)
            text = f"Choose your category:\n{categories_list}"
        else:
            text = "You don't have any categories."
        return self.send_message(text=text, chat_id=chat_id)

    def get_user_categories(self, tg_user_id: int) -> list:
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user.id, is_deleted=False)
        return [category.title for category in categories]

    def create_new_goal(self, tg_user_id: int, goal_title: str, category_title: str):
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        category = GoalCategory.objects.get(board__participants__user=tg_user.user.id, title=category_title)
        Goal.objects.create(
            category=category,
            title=goal_title,
            user=tg_user.user,
        )
