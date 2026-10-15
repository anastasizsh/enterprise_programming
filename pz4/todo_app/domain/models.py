import uuid
from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Optional

class TaskStatus(Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Deadline:
    due_date: date

@dataclass(kw_only=True)
class Entity:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass(kw_only=True)
class Project(Entity):
    name: str

@dataclass(kw_only=True)
class Task(Entity):
    title: str
    project_id: uuid.UUID
    status: TaskStatus = TaskStatus.NEW
    priority: Priority = Priority.MEDIUM
    deadline: Optional[Deadline] = None

    def start(self):
        if self.status == TaskStatus.COMPLETED:
            raise ValueError("Не можна почати вже завершене завдання")
        self.status = TaskStatus.IN_PROGRESS

    def complete(self):
        self.status = TaskStatus.COMPLETED

    def is_overdue(self, current_date: date) -> bool:
        if not self.deadline or self.status == TaskStatus.COMPLETED:
            return False
        return current_date > self.deadline.due_date
    