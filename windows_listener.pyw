import os
import json
import time
import logging
import requests
from dotenv import load_dotenv
from winotify import Notification, audio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOPIC = os.getenv("topic", "").strip()

logging.basicConfig(
    filename=os.path.join(BASE_DIR, "listener.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def send_windows_push(title: str, message: str) -> None:
    toast = Notification(
        app_id="Ai-secretary",
        title=title,
        msg=message,
        duration="short",
    )
    toast.set_audio(audio.Default, loop=False)
    toast.show()


def listen_ntfy() -> None:
    if not TOPIC:
        logging.error("Переменная topic не найдена в файле .env")
        return

    url = f"https://ntfy.sh/{TOPIC}/json"
    logging.info(f"Подключение к потоку уведомлений: {url}")

    while True:
        try:
            with requests.get(url, stream=True, timeout=90) as response:
                response.raise_for_status()
                logging.info("Слушатель запущен и ждёт уведомления с сервера...")

                for line in response.iter_lines():
                    if not line:
                        continue

                    data = json.loads(line.decode("utf-8"))

                    if data.get("event") == "message":
                        title = data.get("title", "Toshiba Server")
                        message = data.get("message", "")
                        logging.info(f"Получен пуш: {title} — {message}")
                        send_windows_push(title, message)

        except requests.RequestException as e:
            logging.warning(f"Обрыв связи ({e}), переподключение через 5 сек...")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Ошибка обработки сообщения: {e}")
            time.sleep(5)


if __name__ == "__main__":
    try:
        listen_ntfy()
    except KeyboardInterrupt:
        logging.info("Слушатель остановлен вручную")