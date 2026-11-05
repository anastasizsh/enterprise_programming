"""This file intentionally contains three mypy errors for practical work 3."""

from uuid import uuid4

from todo_app.domain.domain_types import (
    TaskId,
    TaskStatus,
    UserId,
    create_task,
    get_tasks_by_status,
)


task = create_task(TaskId(uuid4()), "typed task")
wrong_status: TaskStatus = "completed"  # error: Literal does not allow this value
wrong_user: UserId = task.id  # error: TaskId and UserId are distinct NewTypes
wrong_filter = get_tasks_by_status([task], 404)  # error: status must be TaskStatus

print(wrong_status, wrong_user, wrong_filter)
