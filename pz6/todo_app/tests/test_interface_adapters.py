import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from application.use_cases import CreateTask
from interface_adapters.controllers.task_controller import TaskController
from interface_adapters.presenters.task_presenter import TaskPresenter
from interface_adapters.view_models.task_view_models import TaskViewModel, ErrorViewModel

@pytest.fixture
def controller():
    use_case = CreateTask()
    presenter = TaskPresenter()
    dummy_project = MagicMock()
    return TaskController(use_case, presenter, dummy_project)

def test_create_task_success(controller):
    result = controller.create_task(title="Підготувати звіт", description="Завершити звіт до п'ятниці")
    assert isinstance(result, TaskViewModel)
    assert result.title == "Підготувати звіт"
    assert result.status == "new"
    assert result.message == "Завдання успішно створено"

def test_create_task_empty_title(controller):
    result = controller.create_task(title="", description="Опис завдання")
    assert isinstance(result, ErrorViewModel)
    assert result.success is False
    assert result.error_code == "VALIDATION_ERROR"

def test_create_task_whitespace_title(controller):
    result = controller.create_task(title="   ", description="Опис завдання")
    assert isinstance(result, ErrorViewModel)
    assert result.success is False
    assert result.error_code == "VALIDATION_ERROR"