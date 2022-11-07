from bot.models import TgUser
from bot.tg.client import TgClient
from django.core.management.base import BaseCommand
from todolist.settings import TELEGRAM_BOT_TOKEN


class Command(BaseCommand):
    help = 'Receives telegram bot notifications and sends notifications text to user'

    def handle(self, *args, **options):
        offset = 0
        chosen_goal_category = None
        create_command_used = False
        tg_client = TgClient(token=TELEGRAM_BOT_TOKEN, tg_user=TgUser)
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if item.message:
                    tg_user_id = item.message.from_.id
                    chat_id = item.message.chat.id

                    if not tg_client.tg_user_exists(tg_user_id=tg_user_id) or not tg_client.tg_user_verified(tg_user_id=tg_user_id):
                        verification_code = tg_client.generate_verification_code()
                        tg_client.send_verification_code(chat_id=chat_id, verification_code=verification_code)
                        if not tg_client.tg_user_exists(tg_user_id=tg_user_id):
                            tg_client.create_new_tg_user(
                                tg_user_id=tg_user_id,
                                chat_id=chat_id,
                                verification_code=verification_code
                            )
                        elif not tg_client.tg_user_verified(tg_user_id=tg_user_id):
                            tg_client.update_tg_user(tg_user_id=tg_user_id, verification_code=verification_code)
                    else:
                        user_message = item.message.text

                        if user_message == '/goals':
                            tg_client.send_user_goals(tg_user_id=tg_user_id, chat_id=chat_id)
                        elif user_message == '/create':
                            create_command_used = True
                            tg_client.send_user_categories(tg_user_id=tg_user_id, chat_id=chat_id)
                        elif create_command_used and user_message in (tg_client.get_user_categories(tg_user_id=tg_user_id)):
                            chosen_goal_category = user_message
                            tg_client.send_message(chat_id=chat_id, text='Please enter the title of a new goal')
                        elif create_command_used and user_message == '/cancel':
                            chosen_goal_category = None
                            create_command_used = False
                            tg_client.send_message(chat_id=chat_id, text=f'Your request has been cancelled')
                        elif create_command_used and not chosen_goal_category and user_message not in (tg_client.get_user_categories(tg_user_id=tg_user_id)):
                            tg_client.send_message(chat_id=chat_id, text='Please choose the correct category')
                        elif create_command_used:
                            goal_title = user_message
                            tg_client.create_new_goal(tg_user_id=tg_user_id, goal_title=goal_title, category_title=chosen_goal_category)
                            tg_client.send_message(chat_id=chat_id, text=f'Goal "{goal_title}" has been created')
                            chosen_goal_category = None
                            create_command_used = False
                        else:
                            tg_client.send_message(chat_id=chat_id, text='Unknown command.Please try again.')
