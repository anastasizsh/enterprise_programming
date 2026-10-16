from typing import Protocol, Optional
import uuid
from domain.models import Task

class TaskRepository(Protocol):
    def save(self, task: Task) -> None: pass
    def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]: pass
    def get_by_project(self, project_id: uuid.UUID) -> list[Task]: pass
    
    # Методи транзакцій
    def begin(self) -> None: pass
    def commit(self) -> None: pass
    def rollback(self) -> None: pass

class NotificationPort(Protocol):
    def send(self, message: str) -> None: pass