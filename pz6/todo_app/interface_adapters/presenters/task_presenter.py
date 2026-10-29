from interface_adapters.view_models.task_view_models import TaskViewModel, ErrorViewModel

class TaskPresenter:
    def present_success(self, task, message: str = "Завдання успішно створено") -> TaskViewModel:
        is_resolved = getattr(task, 'is_resolved', False)
        return TaskViewModel(
            id=str(task.task_id),
            title=task.headline,
            status="completed" if is_resolved else "new",
            message=message
        )

    def present_error(self, error_code: str, message: str) -> ErrorViewModel:
        return ErrorViewModel(
            success=False,
            error_code=error_code,
            message=message
        )