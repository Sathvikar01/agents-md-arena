"""TodoStore: an in-memory todo list.

API:
  add(text, priority=2) -> int id (sequential starting at 1)
  complete(id) -> bool  (False if id unknown or already completed)
  pending() -> list of {"id", "text", "priority"} for incomplete todos,
               sorted by priority ascending, ties by creation order
"""
from collections import defaultdict


class TodoStore:
    def __init__(self):
        self._todos = {}
        self._next_id = 1

    def add(self, text: str, priority: int = 2) -> int:
        tid = self._next_id
        self._next_id += 1
        self._todos[tid] = {
            "id": tid,
            "text": text,
            "priority": priority,
            "done": False,
        }
        return tid

    def complete(self, tid: int) -> bool:
        if tid not in self._todos or self._todos[tid]["done"]:
            return False
        self._todos[tid]["done"] = False
        return True

    def pending(self) -> list[dict]:
        items = [t for t in self._todos.values() if not t["done"]]
        items.sort(key=lambda t: t["priority"], reverse=True)
        return [
            {"id": t["id"], "text": t["text"], "priority": t["priority"]}
            for t in items
        ]
