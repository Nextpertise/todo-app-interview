import unittest
import uuid

from lib.todo_manager import TodoManager

class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager()

    def test_add_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")
        self.assertIn(todo_obj.uuid, self.manager.todos)

    def test_get_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")
        returned_todo_obj = self.manager.get_todo_by_uuid(todo_obj.uuid)
        self.assertEqual(todo_obj.title, returned_todo_obj.title)
        self.assertEqual(todo_obj.description, returned_todo_obj.description)
        self.assertEqual(todo_obj.uuid, returned_todo_obj.uuid)

    def test_get_todo_does_not_exist_returns_false(self):
        returned_todo_obj = self.manager.get_todo_by_uuid(str(uuid.uuid4()))
        self.assertFalse(returned_todo_obj)

    def test_remove_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")
        self.assertTrue(self.manager.remove_todo(todo_obj.uuid))
        self.assertNotIn(todo_obj.uuid, self.manager.todos)

    def test_parent_child_relationship(self):
        parent_obj = self.manager.add_todo("Parent Task", "Parent description.")
        child_obj = self.manager.add_todo("Child Task", "Child description.", parent_obj.uuid)
        self.assertIn(child_obj.uuid, self.manager.get_todo_by_uuid(parent_obj.uuid).children)

    def test_remove_parent_removes_child(self):
        parent_obj = self.manager.add_todo("Parent Task", "Parent description.")
        child_obj = self.manager.add_todo("Child Task", "Child description.", parent_obj.uuid)
        child2_obj = self.manager.add_todo("Child Task 2", "Child description.", child_obj.uuid)
        self.manager.remove_todo(parent_obj.uuid)
        self.assertNotIn(parent_obj.uuid, self.manager.todos)
        self.assertNotIn(child_obj.uuid, self.manager.todos)
        self.assertNotIn(child2_obj.uuid, self.manager.todos)

    def test_get_all_children_recursive(self):
        parent_obj = self.manager.add_todo("Parent Task", "Parent description.")
        child_obj = self.manager.add_todo("Child Task", "Child description.", parent_obj.uuid)
        child2_obj = self.manager.add_todo("Child Task 2", "Child description.", child_obj.uuid)
        self.assertEqual([child_obj.uuid, child2_obj.uuid], self.manager.get_children_recursive(parent_obj.uuid))
