from typing import List, Literal
from fastapi import FastAPI

from lib.todo_manager import TodoManager
from models import Todo, TodoWithChildren

app = FastAPI()
app.manager = TodoManager()

@app.get("/todo")
async def list_all_todos() -> List[Todo]:
    return app.manager.get_all_todos()


@app.get("/todo/{todo_uuid}")
async def get_todo(todo_uuid: str) -> TodoWithChildren | Literal[False]:
    return app.manager.get_todo_by_uuid(todo_uuid)


@app.post("/todo")
async def add_todo(title: str, description: str, parent_uuid: str = None) -> Todo | dict:
    try:
        result = app.manager.add_todo(title, description, parent_uuid)
    except ValueError as e:
        return {"error": str(e)}
    return result

@app.delete("/todo/{todo_uuid}")
async def remove_todo(todo_uuid: str) -> bool:
    return app.manager.remove_todo(todo_uuid)
