from domain.entities import Task, User, Project

class CreateTask:
    "Сценарій використання: Створення завдання в межах проєкту."
    
    def execute(self, target_project: Project, task_id: int, headline: str, details: str) -> Task:
        new_task = Task(task_id=task_id, headline=headline, details=details)
        target_project.append_new_task(new_task)
        return new_task


class AssignTask:
    "Сценарій використання: Призначення виконавця на конкретне завдання."
    
    def execute(self, target_task: Task, worker: User) -> Task:
        if target_task.is_resolved:
            raise ValueError("Неможливо призначити виконавця на вже закрите завдання.")
        
        target_task.assigned_worker = worker
        return target_task


class CompleteTask:
    "Сценарій використання: Закриття (виконання) завдання."
    
    def execute(self, target_task: Task) -> Task:
        if not target_task.is_resolved:
            target_task.mark_as_resolved()
        return target_task