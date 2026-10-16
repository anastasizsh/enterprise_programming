import uuid
from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Optional, NewType

UserId = NewType('UserId', int)

class TaskStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class Deadline:
    due_date: date

@dataclass(kw_only=True)
class Entity:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass(kw_only=True)
class Task(Entity):
    title: str
    project_id: Optional[uuid.UUID] = None  # ВЕРНУЛИ ПОЛЕ ДЛЯ ПРОЄКТІВ
    status: TaskStatus = TaskStatus.NEW
    assignee_id: Optional[UserId] = None
    deadline: Optional[Deadline] = None

    def start(self):
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Не можна почати вже завершене завдання")
        self.status = TaskStatus.IN_PROGRESS

    def complete(self):
        self.status = TaskStatus.COMPLETED