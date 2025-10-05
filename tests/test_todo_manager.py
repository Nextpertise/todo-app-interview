import random
import unittest

import pytest

from lib.todo_manager import TodoManager
from tests.helpers import build_linear_n, timeit, build_star_tree


class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager()

    def test_0_single_add_and_get_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")

        returned_todo = self.manager.try_get_todo_by_uuid(todo_obj.uuid)
        self.assertIsNotNone(returned_todo)
        self.assertEqual(todo_obj.title, returned_todo.title)
