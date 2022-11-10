from dataclasses import dataclass, field
from typing import List, Optional
from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: str
    last_name: Optional[str]
    type: str
    title: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Optional[Message]

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
