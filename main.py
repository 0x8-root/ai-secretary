'''Главный файл запуска ai-secretary. Здесь иницируется запуск, а также собираются функции'''
import time
from datetime import datetime
from notifier import notify
import database

def main():
    database.init_db()
    print("Ai-secretary запущен")

    title =  input("Введите текст напоминания(Или нажмите Enter, чтобы сразу запустить таймер): ").strip()
    if title:
        remind_time = input("Во сколько выполнить напоминание(В формате 00:00): ").strip()
        priority = input("Введите приоритет от 1-5(ENTER = 3): ").strip() or "3"
        database.add_task(title, remind_time, priority)
        print(f"Сохранено: {title} на {remind_time}, приоритет:{priority}")

    print("Режим ожидания запущен. Для остановки Ctrl+С...")
    while True:
        now_time = datetime.now().strftime("%H:%M")
        tasks = database.get_pending_tasks(now_time)

        for task_id, task_title, task_priority in tasks:
            notify(title="Напоминанинае Ai-secretary", message=task_title, priority=task_priority)
            database.mark_as_sent(task_id)
            print(f"{[now_time]}: Пуш отправлен: {task_title}")

        time.sleep(20)   
        
if __name__ == '__main__':
    main()