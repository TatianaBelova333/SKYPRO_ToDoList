from dataclasses import dataclass, field
from typing import List, Optional
from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    """Sender of the message.

     Attributes:
         id (int): Unique identifier for the Telegram user or bot.
         is_bot (bool): True, if this user is a bot.
         first_name (str): User's or bot's first name.
         last_name (:obj:`str`, optional): Optional. User's or bot's last name.
         username (:obj:`str`, optional): Optional. User's or bot's username.

    """
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    """Telegram Bot API Chat object class.

    Attributes:
        id (int): Unique identifier for this chat.
        first_name (str): Optional. First name of the other party in a private chat.
        last_name (:obj:`str`, optional): Optional. Last name of the other party in a private chat.
        type (str): Type of chat, can be either “private”, “group”, “supergroup” or “channel”.
        title (:obj:`str`, optional): Optional. Title, for supergroups, channels and group chats.

    """
    id: int
    first_name: str
    last_name: Optional[str]
    type: str
    title: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    """Telegram Bot API Message object class.

    Attributes:
        message_id (int): Unique message identifier inside this chat.
        from_ (:obj:`MessageFrom`): MessageFrom class instance.
        chat (:obj:`Chat`): Chat class instance.
        text (:obj:`str`, optional): Optional. For text messages, the actual UTF-8 text of the message.

    """
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    """Telegram Bot API incoming update object.

    Attributes:
        update_id (int): The update's unique identifier.
        message (:obj:`Message`, optional): Message class instance.

    """
    update_id: int
    message: Optional[Message]

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    """Object class for receiving messages from the telegram user.

    Attributes:
        ok (boolean): True if response was succesful. False, otherwise.
        result (:obj:`list` of :obj:`UpdateObj`): Telegram Bot response result.

    """
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    """Object class for sending messages to the telegram user.

    Attributes:
        ok (boolean): True if response was succesful. False, otherwise.
        result (:obj:`list` of :obj:`Message`): Telegram Bot response result.

    """
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
