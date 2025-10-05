import time

from lib.todo_manager import TodoManager


def build_star_tree(manager: TodoManager, parent_count: int, children_per_parent: int):
    parents = [manager.add_todo(f"p-{i}", f"parent-{i}") for i in range(parent_count)]
    children = []
    for p in parents:
        for j in range(children_per_parent):
            children.append(manager.add_todo(f"c-{p.title}-{j}", f"child-{j}", parent_uuid=p.uuid))
    return parents, children

def build_linear_n(manager: TodoManager, n: int):
    todos = [manager.add_todo(f"title-{i}", f"desc-{i}") for i in range(n)]
    return todos


def timeit(fn, repeat=1):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best
