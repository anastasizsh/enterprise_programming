from dataclasses import dataclass
from typing import Optional, Sequence
from domain_types import TaskId, UserId, TaskStatus

@dataclass
class Task:
    id: TaskId
    title: str
    status: TaskStatus
    assignee_id: Optional[UserId] = None

def create_task(task_id: TaskId, title: str) -> Task:
    return Task(id=task_id, title=title, status="new")

def assign_task(task: Task, user_id: UserId) -> Task:
    task.assignee_id = user_id
    task.status = "in_progress"
    return task

def complete_task(task: Task) -> Task:
    task.status = "done"
    return task

def get_tasks_by_status(tasks: Sequence[Task], status: TaskStatus) -> list[Task]:
    return [task for task in tasks if task.status == status]