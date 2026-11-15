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
                is_sent INTEGER DEFAULT 0
            )
            """

       )

def add_task(title: str, remind_time: str, priority: str = "3") -> None: #Функция добавления задачи
    with sqlite3.connect(DB_NAME) as conn:
       conn.execute(
           "INSERT INTO tasks (title, remind_time, priority) VALUES (?, ?, ?)",  #Добавляет в табличку значения из ввода title, remind_time, priority
            (title, remind_time, priority),
       )

def get_pending_tasks(current_time: str) -> list[tuple[int, str, str]]: #Проверка задачи на текущее время
    with sqlite3.connect(DB_NAME) as conn:
       cursor = conn.execute(
           "SELECT id, title, priority FROM tasks WHERE remind_time = ? AND is_sent = 0", #В конце и отправленно присвоено 0
            (current_time,),
       )
       return cursor.fetchall() # Вернуть все значения из таблицы кортежем

def mark_as_sent(task_id: int) -> None: #Функция присваивает после отправки задачи 1 в таблице 
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET is_sent = 1 WHERE id = ?", (task_id,))
