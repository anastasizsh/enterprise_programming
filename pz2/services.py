from abc import ABC, abstractmethod
from typing import List, Optional
from models import Task, User


class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass


class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"[EMAIL] To {recipient}: {message}")


class SmsSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"[SMS] To {recipient}: {message}")


class TaskService:
    def __init__(self, notifier: NotificationSender):
        self.notifier = notifier
        self.tasks: List[Task] = []
        self._current_id = 1

    def create_task(self, title: str, description: str, assignee: Optional[User] = None) -> Task:
        clean_title = title.strip() if title else ""
        if not clean_title:
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self._current_id,
            title=clean_title,
            description=description,
            assignee=assignee
        )
        self.tasks.append(task)
        self._current_id += 1

        if assignee:
            recipient = assignee.email if isinstance(self.notifier, EmailSender) else assignee.phone
            self.notifier.send(recipient, f"New task: {task.title}")

        return task

    def get_tasks(self) -> List[Task]:
        return self.tasks