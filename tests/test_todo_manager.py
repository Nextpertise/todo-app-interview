import unittest
from lib.todo_manager import TodoManager

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager()

    def test_add_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")
        self.assertIn(todo_obj.uuid, self.manager.todos)

    def test_remove_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")
        self.assertTrue(self.manager.remove_todo(todo_obj.uuid))
        self.assertNotIn(todo_obj.uuid, self.manager.todos)

    # def test_parent_child_relationship(self):
    #     parent_obj = self.manager.add_todo("Parent Task", "Parent description.")
    #     child_obj = self.manager.add_todo("Child Task", "Child description.", parent_obj.uuid)
    #     self.assertIn(child_obj.uuid, self.manager.get_todo_by_uuid(parent_obj.uuid).children)
    #
    # def test_remove_parent_removes_child(self):
    #     parent_obj = self.manager.add_todo("Parent Task", "Parent description.")
    #     child_obj = self.manager.add_todo("Child Task", "Child description.", parent_obj.uuid)
    #     self.manager.remove_todo(parent_obj.uuid)
    #     self.assertNotIn(parent_obj.uuid, self.manager.todos)
    #     self.assertNotIn(child_obj.uuid, self.manager.todos)