from random import sample
from string import hexdigits
from typing import Type, NoReturn, Callable
import requests
from bot.models import TgUser
from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
import marshmallow_dataclass
from goals.models import Goal, Status, GoalCategory


class TgClient:
    """Telegram client.

    Attributes:
        token (str): Unique bot authentication token.
        tg_user (:obj:`TgUser`): TgUser instance.
    """

    def __init__(self, token: str, tg_user: Type[TgUser]):
        self.token = token
        self.tg_user = tg_user

    def get_url(self, method: str):
        """Return Telegram Bot API URL address.

        Args:
            method (str): Telegram Bot method.
        Returns:
            Telegram Bot API URL address.
        """
        return f"https://api.telegram.org/bot{self.token}/{method}?"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Receive incoming updates using long polling.

        Args:
            offset (int): Identifier of the first update to be returned.
            timeout (int): Timeout in seconds for long polling.
        """
        url = self.get_url('getUpdates') + f'timeout={timeout}&offset={offset}'
        res = requests.get(url).json()
        res_schema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        return res_schema().load(res)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Send a message to the telegram user.

        """
        url = self.get_url('sendMessage') + f'chat_id={chat_id}&text={text}'
        res = requests.get(url).json()
        res_schema = marshmallow_dataclass.class_schema(SendMessageResponse)
        return res_schema().load(res)

    @staticmethod
    def generate_verification_code() -> str:
        """Generates random 6-character verification code.

        Returns:
            6-character string.
        """
        return ''.join(sample(hexdigits, 6))

    def send_verification_code(self, chat_id: int, verification_code: str) -> SendMessageResponse:
        """Sends a message with the verification code to the telegram user.

        Args:
            chat_id (int): Telegram Chat id.
            verification_code (str): Code for verifying the web application account.
        Returns:
            SendMessageResponse.
        """
        text = f'Hello! Please verify your account with this code {verification_code}'
        return self.send_message(chat_id, text)

    def tg_user_exists(self, tg_user_id: int) -> bool:
        """Checks if telegram user exists in the database.

        Args:
            tg_user_id (int): Telegram User id.

        Returns:
            True if the telegram user exists in the database, False otherwise.
        """
        return self.tg_user.objects.filter(tg_user_id=tg_user_id).exists()

    def tg_user_is_verified(self, tg_user_id: int) -> bool:
        """Checks if telegram user is verified in the database.

        Args:
            tg_user_id (int): Telegram User id.

        Returns:
            True if the telegram user is verified in the database, False otherwise.
        """
        if self.tg_user_exists(tg_user_id):
            return self.tg_user.objects.get(tg_user_id=tg_user_id).is_verified
        return False

    def new_or_unverified_tg_user(self, tg_user_id: int) -> bool:
        """Checks if telegram user exists or is verified in the database.

        Args:
            tg_user_id (int): Telegram User id.

        Returns:
            True if the Telegram user does not exist or is not verified in the database, False otherwise.
        """
        return not self.tg_user_exists(tg_user_id) or not self.tg_user_is_verified(tg_user_id)

    def create_new_tg_user(self, tg_user_id: int, chat_id: int, verification_code: str) -> NoReturn:
        """Creates a new TgUser instance in the database.
        Args:
            tg_user_id (int): Telegram User id.
            chat_id (int): Telegram Chat id.
            verification_code (str): Verification code.

        Returns:
            None.
        """
        self.tg_user.objects.create(tg_user_id=tg_user_id, tg_chat_id=chat_id, verification_code=verification_code)

    def update_verification_code(self, tg_user_id: int, verification_code: str) -> NoReturn:
        """Updates verification code for telegram user in the database

        Args:
            tg_user_id (int): Telegram User id.
            verification_code (str): Verification code.

        Returns:
            None.
        """
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        tg_user.verification_code = verification_code
        tg_user.save()

    def send_user_goals(self, tg_user_id: int, chat_id: int) -> SendMessageResponse:
        """Retrieves user's current goals from the database.

        Args:
            tg_user_id (int): Telegram User id.
            chat_id (int): Telegram chat id.

        Returns:
             SendMessageResponse.
        """
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user.id
        ).exclude(status=Status.archived)
        if goals:
            text = '\n'.join(goal.title for goal in goals)
        else:
            text = "You don't have any planned goals."
        return self.send_message(text=text, chat_id=chat_id)

    def send_user_categories(self, tg_user_id: int, chat_id: int) -> SendMessageResponse:
        """Retrieves user's current goal categories from the database.

        Args:
            tg_user_id (int): Telegram User id.
            chat_id (int): Telegram chat id.

        Returns:
             SendMessageResponse.
        """
        categories = self.get_user_categories(tg_user_id)
        if categories:
            categories_list = '\n'.join(categories)
            text = f"Choose your category:\n{categories_list}"
        else:
            text = "You don't have any categories."
        return self.send_message(text=text, chat_id=chat_id)

    def get_user_categories(self, tg_user_id: int) -> list:
        """Retrieves telegram user's current goal categories from the database
        Args:
            tg_user_id (int): Telegram User id.

        Returns:
            List with category titles or empty list.
        """
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user.id, is_deleted=False)
        return [category.title for category in categories]

    def create_new_goal(self, tg_user_id: int, goal_title: str, category_title: str) -> NoReturn:
        """Creates a new Goal instance.

        Args:
            tg_user_id (int): Telegram User id.
            goal_title (str): Goal title.
            category_title (str): Goal Category title.

        Returns:
             None.
        """
        tg_user = self.tg_user.objects.get(tg_user_id=tg_user_id)
        category = GoalCategory.objects.get(board__participants__user=tg_user.user.id, title=category_title)
        Goal.objects.create(category=category, title=goal_title, user=tg_user.user)

    def handle_new_or_unverified_user(self, chat_id: int, tg_user_id: int):
        """Handles a new or unverified Telegram user.

        Args:
            chat_id (int): Telegram chat id.
            tg_user_id (int): Telegram User id.
        """
        if self.new_or_unverified_tg_user(tg_user_id):
            verification_code = self.generate_verification_code()
            self.send_verification_code(chat_id=chat_id, verification_code=verification_code)
            if not self.tg_user_exists(tg_user_id=tg_user_id):
                self.create_new_tg_user(
                    tg_user_id=tg_user_id,
                    chat_id=chat_id,
                    verification_code=verification_code
                )
            elif not self.tg_user_is_verified(tg_user_id=tg_user_id):
                self.update_verification_code(tg_user_id=tg_user_id, verification_code=verification_code)
