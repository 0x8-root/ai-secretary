import requests
from winotify import Notification, audio
import os
from dotenv import load_dotenv

load_dotenv()
DEFAULT_TOPIC=os.getenv('topic', "")

def send_windows_push(title: str, message: str) -> None:
    toast = Notification(
        app_id = "Ai-secretary",
        title = title,
        msg = message,
        duration="short",
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()

def send_phone_push(topic: str, title: str, message: str) -> None:
    if not topic:
        return
    url = f"https://ntfy.sh/{topic}"
    requests.post(
        url,
        data = message.encode("utf-8"),
        headers = {"title": title.encode("utf-8")},
        timeout = 10,
    )

def notify(title: str, message: str, topic: str = DEFAULT_TOPIC) -> None:
    send_windows_push(title,message)
    if topic:
        send_phone_push(topic, title, message)