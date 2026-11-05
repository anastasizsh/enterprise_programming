from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from todo_app.domain.entities import Project, Task, TaskStatus, User
from todo_app.domain.exceptions import InvalidTaskState, ValidationError
from todo_app.domain.services import TaskPriorityCalculator
from todo_app.domain.value_objects import Deadline, Priority


def test_entities_receive_uuid_identity() -> None:
    user = User(name="Ada", email="ada@example.com")
    project = Project(name="Migration")
    assert user.id != project.id


def test_task_start_moves_new_to_in_progress() -> None:
    task = Task(title="Write report")
    task.start()
    assert task.status is TaskStatus.IN_PROGRESS


def test_task_complete_moves_to_done() -> None:
    task = Task(title="Write report")
    task.complete()
    assert task.status is TaskStatus.DONE


def test_completed_task_cannot_start_again() -> None:
    task = Task(title="Write report")
    task.complete()
    with pytest.raises(InvalidTaskState):
        task.start()


def test_overdue_deadline_is_detected() -> None:
    now = datetime(2026, 1, 2, tzinfo=timezone.utc)
    task = Task(title="Pay invoice", deadline=Deadline(now - timedelta(days=1)))
    assert task.is_overdue(now) is True


def test_done_task_is_not_overdue() -> None:
    now = datetime(2026, 1, 2, tzinfo=timezone.utc)
    task = Task(title="Pay invoice", deadline=Deadline(now - timedelta(days=1)))
    task.complete()
    assert task.is_overdue(now) is False


def test_priority_calculator_prioritizes_overdue_tasks() -> None:
    now = datetime(2026, 1, 2, tzinfo=timezone.utc)
    overdue = Task(title="Urgent", priority=Priority.HIGH, deadline=Deadline(now - timedelta(days=1)))
    normal = Task(title="Normal", priority=Priority.LOW)
    calculator = TaskPriorityCalculator()
    assert calculator.calculate(overdue, now) > calculator.calculate(normal, now)


def test_project_tracks_task_ids() -> None:
    project = Project(name="Research")
    task_id = uuid4()
    project.add_task(task_id)
    assert task_id in project.task_ids
    project.remove_task(task_id)
    assert task_id not in project.task_ids


def test_invalid_entity_title_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Task(title=" ")
