import os
import requests
from dotenv import load_dotenv
from winotify import Notification, audio

load_dotenv()
DEFAULT_TOPIC = os.getenv("topic", "")


def send_windows_push(title: str, message: str) -> None:
    toast = Notification(
        app_id="Ai-secretary",
        title=title,
        msg=message,
        duration="short",
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()


def send_phone_push(topic: str, title: str, message: str, priority: str = "3") -> None:
    if not topic:
        return
    url = f"https://ntfy.sh/{topic}"
    requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": title.encode("utf-8"),
            "Priority": priority,
            "Tags": "robot",
        },
        timeout=10,
    )


def notify(title: str, message: str, priority: str = "3", topic: str = DEFAULT_TOPIC) -> None:
    send_windows_push(title, message)
    if topic:
        send_phone_push(topic, title, message, priority=priority)