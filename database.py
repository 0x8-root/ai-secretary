import sqlite3

DB_NAME="secretary.db" #Имя базы даных 

def init_db() -> None:#Функция создания таблицы(возращает ничего)
    with sqlite3.connect(DB_NAME) as conn:#Стандартное подключение таблицы
       conn.execute( #Ввод данных в таблицу
           """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                remind_time TEXT NOT NULL,
                priority TEXT DEFAULT '3',
                task_type TEXT NOT NULL,
                days_of_week TEXT DEFAULT '',
                is_sent INTEGER DEFAULT 0
            )
            """

       )

def add_task(title: str, remind_time: str, task_type: str, days_of_week: str = "", priority: str = "3") -> None: #Функция добавления задачи
    with sqlite3.connect(DB_NAME) as conn:
       conn.execute(
           "INSERT INTO tasks (title, remind_time, task_type, days_of_week, priority) VALUES (?, ?, ?, ?, ?)",  #Добавляет в табличку значения из ввода title, remind_time, priority
            (title, remind_time, task_type, days_of_week, priority),
       )

def get_pending_tasks(current_time: str, current_weekday: int) -> list[tuple[int, str, str]]: #Проверка задачи на текущее время
    with sqlite3.connect(DB_NAME) as conn:
       cursor = conn.execute(
           "SELECT id, title, priority, task_type, days_of_week FROM tasks WHERE remind_time = ? AND is_sent = 0", #В конце и отправленно присвоено 0
            (current_time,),
       )
       rows = cursor.fetchall() # Вернуть все значения из таблицы кортежем
       result = []
       for task_id, title, priority, task_type, days_of_week in rows:
           if task_type != "weekly" or str(current_weekday) in days_of_week.split(","):
               result.append((task_id, title, priority))
       return result
               

def mark_as_sent(task_id: int) -> None: #Функция присваивает после отправки задачи 1 в таблице 
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET is_sent = 1 WHERE id = ?", (task_id,))

def reset_recurring_tasks() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET is_sent = 0 WHERE task_type IN ('daily', 'weekly')")

def get_all_tasks() -> list[dict]:
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory= sqlite3.Row
        cursor = conn.execute("SELECT id, title, remind_time, priority, task_type, days_of_week, is_sent FROM tasks ORDER BY remind_time ASC")
        return [dict(row) for row in cursor.fetchall()]

def delete_task(task_id: int) -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))