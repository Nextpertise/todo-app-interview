import unittest
import uuid

from lib.todo_manager import TodoManager

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager()

    def test_add_and_get_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")

        returned_todo = self.manager.try_get_todo_by_uuid(todo_obj.uuid)
        self.assertIsNotNone(returned_todo)
        self.assertEqual(todo_obj.title, returned_todo.title)

    def test_get_todo_does_not_exist_returns_none(self):
        # Add some random items to the list
        self.manager.add_todo("Test Task", "This is a test.")
        self.manager.add_todo("Test Task 2", "This is another test.")
        self.manager.add_todo("Test Task 3", "More teeeeests")

        returned_todo_obj = self.manager.try_get_todo_by_uuid(uuid.uuid4())
        self.assertIsNone(returned_todo_obj)

    def test_remove_todo(self):
        # Add some random items to the list
        todo1 = self.manager.add_todo("Test Task", "This is a test.")
        todo2 = self.manager.add_todo("Test Task 2", "This is another test.")
        todo3 = self.manager.add_todo("Test Task 3", "More teeeeests")

        self.assertTrue(self.manager.remove_todo(todo2.uuid))
        self.assertIsNone(self.manager.try_get_todo_by_uuid(todo2.uuid))
        self.assertIsNotNone(self.manager.try_get_todo_by_uuid(todo1.uuid))
        self.assertIsNotNone(self.manager.try_get_todo_by_uuid(todo3.uuid))


