from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar, Optional
import uuid
from domain.models import Task
from application.interfaces import TaskRepository, NotificationPort

class ErrorCode(Enum):
    NOT_FOUND = "not_found"
    VALIDATION_ERROR = "validation_error"

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    is_success: bool
    data: Optional[T] = None
    error: Optional[ErrorCode] = None
    error_message: str = ""

    @classmethod
    def ok(cls, data: T):
        return cls(is_success=True, data=data)

    @classmethod
    def fail(cls, error: ErrorCode, message: str):
        return cls(is_success=False, error=error, error_message=message)

@dataclass
class CreateTaskDTO:
    title: str

@dataclass
class CompleteTaskDTO:
    task_id: uuid.UUID

@dataclass
class CompleteProjectDTO:
    project_id: uuid.UUID

@dataclass
class TaskResponseDTO:
    id: uuid.UUID
    title: str
    status: str

# --- USE CASES ---
class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, req: CreateTaskDTO) -> Result[TaskResponseDTO]:
        if not req.title.strip():
            return Result.fail(ErrorCode.VALIDATION_ERROR, "Назва завдання не може бути порожньою")
        
        task = Task(title=req.title)
        self.repository.save(task)
        
        return Result.ok(TaskResponseDTO(id=task.id, title=task.title, status=task.status.value))

class CompleteTaskUseCase:
    def __init__(self, repository: TaskRepository, notifier: NotificationPort):
        self.repository = repository
        self.notifier = notifier

    def execute(self, req: CompleteTaskDTO) -> Result[TaskResponseDTO]:
        task = self.repository.get_by_id(req.task_id)
        if not task:
            return Result.fail(ErrorCode.NOT_FOUND, f"Завдання з ID {req.task_id} не знайдено")
        
        task.complete()
        self.repository.save(task)
        self.notifier.send(f"Завдання '{task.title}' виконано!")
        
        return Result.ok(TaskResponseDTO(id=task.id, title=task.title, status=task.status.value))

class CompleteProjectUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, req: CompleteProjectDTO) -> Result[str]:
        tasks = self.repository.get_by_project(req.project_id)
        if not tasks:
            return Result.fail(ErrorCode.NOT_FOUND, "Завдань для цього проєкту не знайдено")

        self.repository.begin()
        try:
            for task in tasks:
                #special case
                if task.title == "Зламати транзакцію":
                    raise Exception("Імітація збою бази даних!")
                
                task.complete()
                self.repository.save(task)
                
            self.repository.commit()
            return Result.ok(f"Проєкт успішно завершено. Закрито завдань: {len(tasks)}")
            
        except Exception as e:
            self.repository.rollback()
            return Result.fail(ErrorCode.VALIDATION_ERROR, f"Транзакцію скасовано: {str(e)}")