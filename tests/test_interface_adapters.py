from todo_app.application.common import ErrorCode
from todo_app.application.use_cases import CreateTaskUseCase
from todo_app.infrastructure.repositories import InMemoryTaskRepository
from todo_app.interface_adapters import TaskController, TaskPresenter


def make_controller() -> TaskController:
    repository = InMemoryTaskRepository()
    return TaskController(CreateTaskUseCase(repository), TaskPresenter())


def test_controller_returns_task_view_model_for_valid_input() -> None:
    result = make_controller().create_task("Підготувати звіт", "До п'ятниці")
    assert result.id
    assert result.title == "Підготувати звіт"
    assert result.status == "new"
    assert result.message


def test_controller_returns_validation_error_for_empty_title() -> None:
    result = make_controller().create_task("", "Опис")
    assert result.success is False
    assert result.error_code == ErrorCode.VALIDATION_ERROR.value


def test_controller_returns_validation_error_for_whitespace_title() -> None:
    result = make_controller().create_task("   ", "Опис")
    assert result.success is False
    assert result.error_code == "VALIDATION_ERROR"
