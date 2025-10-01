import random
import unittest

import pytest

from lib.todo_manager import TodoManager
from tests.helpers import build_linear_n, timeit, build_star_tree


class TestTodoManager(unittest.TestCase):
    def setUp(self):
        self.manager = TodoManager()

    def test_single_add_and_get_todo(self):
        todo_obj = self.manager.add_todo("Test Task", "This is a test.")

        returned_todo = self.manager.try_get_todo_by_uuid(todo_obj.uuid)
        self.assertIsNotNone(returned_todo)
        self.assertEqual(todo_obj.title, returned_todo.title)

    def test_1_remove_todo(self):
        # Add some random items to the list
        todo1 = self.manager.add_todo("Test Task", "This is a test.")
        todo2 = self.manager.add_todo("Test Task 2", "This is another test.")
        todo3 = self.manager.add_todo("Test Task 3", "More teeeeests")

        self.assertTrue(self.manager.remove_todo(todo2.uuid))
        self.assertIsNone(self.manager.try_get_todo_by_uuid(todo2.uuid))
        self.assertIsNotNone(self.manager.try_get_todo_by_uuid(todo1.uuid))
        self.assertIsNotNone(self.manager.try_get_todo_by_uuid(todo3.uuid))

    def test_2_add_todo_with_parent(self):
        parent_todo = self.manager.add_todo("Parent Task", "This is a parent task.")
        child_todo = self.manager.add_todo("Child Task", "This is a child task.", parent_todo.uuid)
        returned_child_todo = self.manager.try_get_todo_by_uuid(child_todo.uuid)
        self.assertEqual(returned_child_todo.parent_uuid, parent_todo.uuid)


    def test_3_todo_with_same_title_should_fail(self):
        self.manager.add_todo("Test Task 1", "This is a test.")
        todo_obj = self.manager.add_todo("Test Task 2", "This is another test.")

        with self.assertRaises(ValueError):
            self.manager.add_todo("Test Task 2", "Test number 3")

        self.manager.remove_todo(todo_obj.uuid)
        self.manager.add_todo("Test Task 2", "Test number 3")

    def test_4_editing_todo_outside_of_manager_should_not_change_todo_inside(self):
        todo1 = self.manager.add_todo("Test Task 1", "This is a test.")
        todo1_returned = self.manager.try_get_todo_by_uuid(todo1.uuid)
        todo1_returned.title = "Test Task 1 edited"
        todo1_returned_2 = self.manager.try_get_todo_by_uuid(todo1.uuid)
        self.assertEqual(todo1_returned_2.title, "Test Task 1")

        todo2 = self.manager.add_todo("Test Task 2", "This is a test.")
        todo2.title = "Test Task 2 edited"
        returned_todo = self.manager.try_get_todo_by_uuid(todo2.uuid)
        self.assertEqual(returned_todo.title, "Test Task 2")

        todo3 = self.manager.add_todo("Test Task 3", "This is a test.")
        all_todos = self.manager.get_all_todos()
        todo3_returned = [t for t in all_todos if t.uuid == todo3.uuid][0]
        todo3_returned.title = "Test Task 3 edited"
        todo3_returned_2 = self.manager.try_get_todo_by_uuid(todo3.uuid)
        self.assertEqual(todo3_returned_2.title, "Test Task 3")

    def test_5_get_children(self):
        parent_todo = self.manager.add_todo("Parent Task", "This is a parent task.")
        child_todo = self.manager.add_todo("Child Task", "This is a child task.", parent_todo.uuid)
        child_todo_2 = self.manager.add_todo("Child Task 2", "This is a child task 2.", parent_todo.uuid)
        child_todo_3 = self.manager.add_todo("Child Task 3", "This is a child task 3.", parent_todo.uuid)
        _unrelevant_parent_todo_1 = self.manager.add_todo("Unrelevant Parent Task 1", "This is an unrelevant parent task.")
        _unrelevant_child_todo_1 = self.manager.add_todo("Unrelevant Child Task 1", "This is an unrelevant child task.", _unrelevant_parent_todo_1.uuid)
        _unrelevant_parent_todo_2 = self.manager.add_todo("Unrelevant Parent Task 2", "This is an unrelevant parent task.")
        _unrelevant_child_todo_2 = self.manager.add_todo("Unrelevant Child Task 2", "This is an unrelevant child task.", _unrelevant_parent_todo_2.uuid)

        children = self.manager.get_children(parent_todo.uuid)
        self.assertEqual(len(children), 3)
        self.assertIn(child_todo.uuid, children)
        self.assertIn(child_todo_2.uuid, children)
        self.assertIn(child_todo_3.uuid, children)

    def test_6_get_children_recursive(self):
        todo_1 = self.manager.add_todo("1", "grandparent")
        todo_2 = self.manager.add_todo("2", "parent", parent_uuid=todo_1.uuid)
        todo_3 = self.manager.add_todo("3", "second parent", parent_uuid=todo_1.uuid)
        todo_4 = self.manager.add_todo("4", "child", parent_uuid=todo_2.uuid)
        todo_5 = self.manager.add_todo("5", "child", parent_uuid=todo_3.uuid)
        todo_6 = self.manager.add_todo("6", "grandchild 1", parent_uuid=todo_4.uuid)
        todo_7 = self.manager.add_todo("7", "grandchild 2", parent_uuid=todo_5.uuid)
        _unrelevant_todo_1 = self.manager.add_todo("8", "unrelevant parent 1")
        _unrelevant_todo_2 = self.manager.add_todo("9", "unrelevant parent 2", parent_uuid=_unrelevant_todo_1.uuid)
        _unrelevant_todo_3 = self.manager.add_todo("10", "unrelevant todo")

        children = self.manager.get_children_recursive(todo_1.uuid)
        self.assertEqual(len(children), 6)
        self.assertIn(todo_2.uuid, children)
        self.assertIn(todo_3.uuid, children)
        self.assertIn(todo_4.uuid, children)
        self.assertIn(todo_5.uuid, children)
        self.assertIn(todo_6.uuid, children)
        self.assertIn(todo_7.uuid, children)

    @pytest.mark.timeout(5)
    def test_7_perf_lookup_try_get_todo_by_uuid_scaling(self):
        N_SMALL = 5_000
        N_LARGE = 50_000

        manager_small = TodoManager()
        todos_small = build_linear_n(manager_small, N_SMALL)

        manager_large = TodoManager()
        todos_large = build_linear_n(manager_large, N_LARGE)

        sample_small = [t.uuid for t in random.sample(todos_small, k=200)]
        sample_large = [t.uuid for t in random.sample(todos_large, k=200)]

        def lookup_small():
            for u in sample_small:
                assert manager_small.try_get_todo_by_uuid(u) is not None

        def lookup_large():
            for u in sample_large:
                assert manager_large.try_get_todo_by_uuid(u) is not None


        t_small = timeit(lookup_small, repeat=3)
        t_large = timeit(lookup_large, repeat=3)
        ratio = t_large / max(t_small, 1e-9)

        assert ratio < 3.0, f"Too much slow down for large amounts of todos: {ratio}"

    @pytest.mark.timeout(5)
    def test_8_perf_get_children_scaling(self):
        PARENTS_SMALL = 300
        CHILDREN_PER_PARENT_SMALL = 10  # total ~3k
        PARENTS_LARGE = 300
        CHILDREN_PER_PARENT_LARGE = 100  # total ~30k

        manager_small = TodoManager()
        parents_small, _ = build_star_tree(manager_small, PARENTS_SMALL, CHILDREN_PER_PARENT_SMALL)

        manager_large = TodoManager()
        parents_large, _ = build_star_tree(manager_large, PARENTS_LARGE, CHILDREN_PER_PARENT_LARGE)

        sample_small = random.sample(parents_small, k=50)
        sample_large = random.sample(parents_large, k=50)

        def fetch_small():
            for p in sample_small:
                children = manager_small.get_children(p.uuid)
                assert len(children) == CHILDREN_PER_PARENT_SMALL

        def fetch_large():
            for p in sample_large:
                children = manager_large.get_children(p.uuid)
                assert len(children) == CHILDREN_PER_PARENT_LARGE

        t_small = timeit(fetch_small, repeat=3)
        t_large = timeit(fetch_large, repeat=3)

        ratio = t_large / max(t_small, 1e-9)
        assert ratio < 6.0, f"get_children scaled too poorly: {ratio:.2f}x"

