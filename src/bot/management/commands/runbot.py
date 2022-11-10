from bot.models import TgUser
from bot.tg.client import TgClient
from django.core.management.base import BaseCommand
from todolist.settings import TELEGRAM_BOT_TOKEN


class Command(BaseCommand):
    help = 'Receives telegram bot notifications and sends notifications text to user'
    chosen_goal_category = None
    create_command_used = False
    bot_commands = ['/goals', '/create', '/cancel']

    def _process_standard_commands(self, tg_client, user_message, tg_user_id, chat_id):
        if user_message == '/goals':
            tg_client.send_user_goals(tg_user_id=tg_user_id, chat_id=chat_id)
        elif user_message == '/create':
            self.create_command_used = True
            tg_client.send_user_categories(tg_user_id=tg_user_id, chat_id=chat_id)
        elif user_message == '/cancel':
            self.chosen_goal_category = None
            self.create_command_used = False
            tg_client.send_message(chat_id=chat_id, text=f'Your request has been cancelled')

    def _process_other_commands(self, tg_client, user_message, tg_user_id, chat_id):
        if self.create_command_used and user_message in (tg_client.get_user_categories(tg_user_id=tg_user_id)):
            self.chosen_goal_category = user_message
            tg_client.send_message(chat_id=chat_id, text='Please enter the title of a new goal')
        elif self.create_command_used and not self.chosen_goal_category and user_message not in (
            tg_client.get_user_categories(tg_user_id=tg_user_id)):
            tg_client.send_message(chat_id=chat_id, text='Please choose the correct category')
        elif self.create_command_used:
            goal_title = user_message
            tg_client.create_new_goal(tg_user_id=tg_user_id, goal_title=goal_title, category_title=self.chosen_goal_category)
            tg_client.send_message(chat_id=chat_id, text=f'Goal "{goal_title}" has been created')
            self.chosen_goal_category = None
            self.create_command_used = False
        else:
            tg_client.send_message(chat_id=chat_id, text='Unknown command.Please try again.')

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(token=TELEGRAM_BOT_TOKEN, tg_user=TgUser)
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if item.message:
                    tg_user_id = item.message.from_.id
                    chat_id = item.message.chat.id

                    if tg_client.new_or_unverified_tg_user(tg_user_id=tg_user_id):
                        tg_client.handle_new_or_unverified_user(tg_user_id=tg_user_id, chat_id=chat_id)
                    else:
                        user_message = item.message.text

                        if user_message in self.bot_commands:
                            self._process_standard_commands(tg_client, user_message, tg_user_id, chat_id)
                        else:
                            self._process_other_commands(tg_client, user_message, tg_user_id, chat_id)
