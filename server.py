from fastapi import FastAPI
from pydantic import BaseModel
from database import add_task, init_db, get_all_tasks, delete_task 

init_db()

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    remind_time: str
    task_type: str = "once"
    days_of_week: str = ""
    priority: int = 3


@app.get("/")
def read_root():
    return { "Hello": "world" }
    
@app.get("/tasks/{task_id}")
def read_task(task_id: int, q: str | None = None):
    return {"task_id": task_id, "q": q}

@app.get("/tasks")
def read_task():
    return get_all_tasks()

@app.post("/tasks")
def create_tasks(task: TaskCreate):
    add_task(task.title, task.remind_time, task.task_type, task.days_of_week, task.priority)
    return {"status": "ok"}

@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    delete_task(task_id)
    return {"status": "deleted"}