from typing import Optional
import uuid
import copy
from domain.models import Task
from application.interfaces import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._storage: dict[uuid.UUID, Task] = {}
        self._transaction_backup: dict[uuid.UUID, Task] = {}
        self._in_transaction = False

    def save(self, task: Task) -> None:
        self._storage[task.id] = task

    def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        return self._storage.get(task_id)

    def get_by_project(self, project_id: uuid.UUID) -> list[Task]:
        return [task for task in self._storage.values() if task.project_id == project_id]

    def begin(self) -> None:
        self._in_transaction = True
        self._transaction_backup = copy.deepcopy(self._storage)

    def commit(self) -> None:
        self._in_transaction = False
        self._transaction_backup = {}

    def rollback(self) -> None:
        if self._in_transaction:
            self._storage = self._transaction_backup
            self._in_transaction = False
            self._transaction_backup = {}