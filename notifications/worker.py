from typing import Any, TypedDict

from .tasks import create_event, create_notification, read_notification


class Message(TypedDict):
    type: str
    payload: Any


def execute_message(data: Message) -> Message:
    if data["type"] == "create-event":
        create_event(data["payload"])
    if data["type"] == "create-notification":
        create_notification(data["payload"])
    if data["type"] == "read-notification":
        read_notification(data["payload"])
    return data

    raise Exception("Invalid message")