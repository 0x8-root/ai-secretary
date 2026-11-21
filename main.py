'''Главный файл запуска ai-secretary. Здесь иницируется запуск, а также собираются функции'''
import time
from datetime import datetime
from notifier import notify
import database
import uvicorn
import threading

def main():
    database.init_db()
    threading.Thread(target=run_server, daemon=True).start()
    print("Ai-secretary запущен")

    print("Режим ожидания запущен. Для остановки Ctrl+С...")
    last_reset_date = None
    while True:
        now = datetime.now()
        now_time = now.strftime("%H:%M")
        now_weekday = now.weekday()
        tasks = database.get_pending_tasks(now_time, now_weekday)

        if now_time == "00:00" and last_reset_date != now.date():
            database.reset_recurring_tasks()
            last_reset_date = now.date()
        for task_id, task_title, task_priority in tasks:
            notify(title="Напоминание Ai-secretary", message=task_title, priority=task_priority)
            database.mark_as_sent(task_id)
            print(f"[{now_time}]: Пуш отправлен: {task_title}")

        if now_time == "00:00" and last_reset_date != now.date():
            database.reset_recurring_tasks()
            
        time.sleep(20)  

def run_server():
    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="warning")
  
        
if __name__ == '__main__':
    main()