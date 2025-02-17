from models import Todo

class TodoManager:
    def __init__(self):
        self.todos = {}

    def add_todo(self, title: str, description: str, parent_uuid: str = None) -> Todo:
        if parent_uuid and parent_uuid not in self.todos:
            raise ValueError(f"Parent todo with uuid {parent_uuid} does not exist.")
        todo = Todo(
            title=title,
            description=description,
            parent_uuid=parent_uuid
        )
        self.todos[todo.uuid] = todo
        return todo

    def remove_todo(self, todo_uuid: str) -> bool:
        if todo_uuid in self.todos:
            del self.todos[todo_uuid]
            return True
        return False

    def get_all_todos(self):
        return list(self.todos.values())
