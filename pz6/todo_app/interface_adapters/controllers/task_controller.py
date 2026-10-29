import random
from application.use_cases import CreateTask
from interface_adapters.presenters.task_presenter import TaskPresenter

class TaskController:
    def __init__(self, use_case: CreateTask, presenter: TaskPresenter, default_project):
        self.use_case = use_case
        self.presenter = presenter
        self.default_project = default_project

    def create_task(self, title: str, description: str = ""):
        if not title or not title.strip():
            return self.presenter.present_error("VALIDATION_ERROR", "Назва завдання не може бути порожньою")

        task_id = random.randint(1, 10000)
        
        try:
            result_task = self.use_case.execute(
                target_project=self.default_project,
                task_id=task_id,
                headline=title.strip(),
                details=description
            )
            return self.presenter.present_success(result_task)
        except Exception as e:
            return self.presenter.present_error("VALIDATION_ERROR", str(e))