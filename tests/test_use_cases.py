from uuid import uuid4

from todo_app.application.common import ErrorCode
from todo_app.application.dto import AssignTaskRequest, TaskRequest
from todo_app.application.use_cases import AssignTaskUseCase, CompleteTaskUseCase, CreateTaskUseCase
from todo_app.infrastructure.notifications import SmsSender
from todo_app.infrastructure.repositories import InMemoryTaskRepository
from todo_app.domain.services import TaskNotificationService


def test_create_task_success_and_fake_repository() -> None:
    repository = InMemoryTaskRepository()
    result = CreateTaskUseCase(repository).execute(TaskRequest(title="Prepare report"))
    assert result.success is True
    assert result.value is not None
    assert repository.get(result.value.task_id) is not None


def test_create_task_rejects_empty_title_with_validation_error() -> None:
    result = CreateTaskUseCase(InMemoryTaskRepository()).execute(TaskRequest(title=" "))
    assert result.success is False
    assert result.error_code is ErrorCode.VALIDATION_ERROR


def test_complete_task_returns_not_found() -> None:
    result = CompleteTaskUseCase(InMemoryTaskRepository()).execute(uuid4())
    assert result.success is False
    assert result.error_code is ErrorCode.NOT_FOUND


def test_assign_task_sends_notification_through_injected_sender() -> None:
    repository = InMemoryTaskRepository()
    created = CreateTaskUseCase(repository).execute(TaskRequest(title="Assign me"))
    task_id = created.value.task_id if created.value else uuid4()
    sender = SmsSender()
    service = TaskNotificationService(sender)
    result = AssignTaskUseCase(repository, notification_service=service).execute(
        AssignTaskRequest(task_id, uuid4(), "+10000000000")
    )
    assert result.success is True
    assert len(sender.sent_messages) == 1
