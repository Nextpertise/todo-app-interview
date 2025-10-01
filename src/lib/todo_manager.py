from copy import copy
from typing import Literal

from models import Todo, TodoWithChildren


class TodoManager:
    def __init__(self):
        root_no_children = Todo(title="title2", description="I am the root")
        parent = Todo(title="title1", description="I am the root and I have children")
        child_1 = Todo(title="title1a", description="", parent_uuid=parent.uuid)
        child_2 = Todo(title="title1b", description="", parent_uuid=child_1.uuid)

        self.todos: dict[str, Todo] = {
            root_no_children.uuid: root_no_children,
            parent.uuid: parent,
            child_1.uuid: child_1,
            child_2.uuid: child_2,
        }

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

    def get_todo_by_uuid(self, todo_uuid: str) -> TodoWithChildren | Literal[False]:
        todo = self.todos.get(todo_uuid, False)
        if not todo:
            return False

        children = self.get_children(todo_uuid)
        todo_with_children = TodoWithChildren.model_validate(todo.model_dump())
        todo_with_children.children.extend(children)
        return todo_with_children

    def remove_todo(self, todo_uuid: str) -> bool:
        todo = self.get_todo_by_uuid(todo_uuid)
        if not todo:
            return False

        for todo_child_uuid in todo.children:
            self.remove_todo(todo_child_uuid)

        self.todos.pop(todo_uuid, None)
        return True

    def get_all_todos(self):
        return list(self.todos.values())

    def get_children(self, parent_uuid: str) -> list[str]:
        return [todo.uuid for todo in self.todos.values() if todo.parent_uuid == parent_uuid]

    def get_children_recursive(self, parent_uuid: str) -> list[str]:
        children = self.get_children(parent_uuid)
        all_children = copy(children)
        for child_uuid in children:
            all_children.extend(self.get_children_recursive(child_uuid))
        return all_children

