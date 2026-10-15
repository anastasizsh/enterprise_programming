from abc import ABC, abstractmethod
import uuid
from typing import Optional
from .models import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def get_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        pass
        
    @abstractmethod
    def get_all(self) -> list[Task]:
        pass