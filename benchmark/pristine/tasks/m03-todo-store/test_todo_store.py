from todo_store import TodoStore


def test_ids_sequential():
    s = TodoStore()
    assert s.add("a") == 1 and s.add("b") == 2


def test_pending_initially_contains_todo():
    s = TodoStore()
    s.add("task")
    p = s.pending()
    assert len(p) == 1 and p[0]["text"] == "task"


def test_complete_removes_from_pending():
    s = TodoStore()
    i = s.add("task")
    assert s.complete(i) is True
    assert s.pending() == []


def test_double_complete_false():
    s = TodoStore()
    i = s.add("task")
    s.complete(i)
    assert s.complete(i) is False


def test_unknown_id_false():
    s = TodoStore()
    assert s.complete(99) is False


def test_pending_sorted_priority_asc_then_creation():
    s = TodoStore()
    s.add("low", priority=5)
    s.add("high", priority=1)
    s.add("mid-a", priority=3)
    s.add("mid-b", priority=3)
    assert [t["id"] for t in s.pending()] == [2, 3, 4, 1]


def test_pending_fields():
    s = TodoStore()
    s.add("write docs", priority=4)
    assert s.pending() == [{"id": 1, "text": "write docs", "priority": 4}]


def test_completed_excluded_but_store_keeps_others():
    s = TodoStore()
    a = s.add("a")
    s.add("b")
    s.complete(a)
    assert [t["text"] for t in s.pending()] == ["b"]
