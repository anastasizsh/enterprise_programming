from uuid import UUID

from todo_app.bootstrap import create_application
from todo_app.interface_adapters.view_models import TaskViewModel


def test_full_create_get_complete_flow() -> None:
    application = create_application()
    created = application.controller.create_task("Підготувати звіт", "Здати вчасно")
    assert isinstance(created, TaskViewModel)
    task_id = UUID(created.id)
    found = application.get_task.execute(task_id)
    assert found.success is True
    assert found.value and found.value.status == "new"
    completed = application.complete_task.execute(task_id)
    assert completed.success is True
    verified = application.get_task.execute(task_id)
    assert verified.value and verified.value.status == "done"


def test_list_use_case_reads_saved_tasks() -> None:
    application = create_application()
    application.controller.create_task("One", "")
    application.controller.create_task("Two", "")
    result = application.list_tasks.execute()
    assert result.success is True
    assert len(result.value or []) == 2


def test_use_case_accepts_an_alternative_repository() -> None:
    class RecordingRepository:
        def __init__(self) -> None:
            self.items = {}

        def save(self, task):
            self.items[task.id] = task
            return task

        def get(self, task_id):
            return self.items.get(task_id)

        def list_all(self):
            return list(self.items.values())

        def delete(self, task_id):
            return self.items.pop(task_id, None) is not None

    repository = RecordingRepository()
    app = create_application(repository=repository)
    created = app.controller.create_task("Stored elsewhere", "")
    assert isinstance(created, TaskViewModel)
    assert len(repository.items) == 1
