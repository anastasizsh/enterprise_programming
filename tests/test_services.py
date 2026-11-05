from uuid import uuid4

from todo_app.domain.entities import Task
from todo_app.domain.services import TaskAssignmentService, TaskNotificationService


class FakeSender:
    def __init__(self) -> None:
        self.messages: list[tuple[str, str, str]] = []

    def send(self, recipient: str, subject: str, message: str) -> None:
        self.messages.append((recipient, subject, message))


def test_notification_service_uses_injected_fake_sender() -> None:
    sender = FakeSender()
    service = TaskNotificationService(sender)
    task = Task(title="Review pull request")
    service.notify_assignment(task, "developer@example.com")
    assert len(sender.messages) == 1
    assert sender.messages[0][0] == "developer@example.com"
    assert "Review pull request" in sender.messages[0][1]


def test_assignment_service_changes_only_assignment_responsibility() -> None:
    task = Task(title="Review pull request")
    assignee = uuid4()
    TaskAssignmentService().assign(task, assignee)
    assert task.assignee_id == assignee
