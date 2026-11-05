from uuid import uuid4

from todo_app.domain.domain_types import (
    TaskId,
    UserId,
    assign_task,
    complete_task,
    create_task,
    get_tasks_by_status,
)


def test_typed_domain_functions() -> None:
    task = create_task(TaskId(uuid4()), "Typed task")
    assigned = assign_task(task, UserId(uuid4()))
    completed = complete_task(assigned)
    assert completed.status == "done"
    assert get_tasks_by_status([completed], "done") == [completed]
