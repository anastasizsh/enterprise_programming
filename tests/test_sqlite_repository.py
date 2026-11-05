from pathlib import Path

from todo_app.application.dto import TaskRequest
from todo_app.application.use_cases import CompleteTaskUseCase, CreateTaskUseCase
from todo_app.infrastructure.repositories import SQLiteTaskRepository


def test_sqlite_repository_preserves_task_and_status(tmp_path: Path) -> None:
    repository = SQLiteTaskRepository(tmp_path / "tasks.sqlite3")
    created = CreateTaskUseCase(repository).execute(TaskRequest(title="Persist me"))
    assert created.value is not None
    task_id = created.value.task_id
    assert repository.get(task_id) is not None
    completed = CompleteTaskUseCase(repository).execute(task_id)
    assert completed.value and completed.value.status == "done"
    assert repository.get(task_id) is not None
    assert repository.get(task_id).status.value == "done"
    repository.close()
