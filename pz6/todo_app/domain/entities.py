from datetime import datetime
from typing import List, Optional

class User:
    "Сутність користувача в системі."
    
    def __init__(self, user_id: int, full_name: str, email_address: str):
        self.user_id = user_id
        self.full_name = full_name
        self.email_address = email_address

    def __repr__(self) -> str:
        return f"<User: {self.full_name}>"


class Task:
    "Сутність конкретного робочого завдання."
    
    def __init__(self, task_id: int, headline: str, details: str):
        self.task_id = task_id
        self.headline = headline
        self.details = details
        self.is_resolved: bool = False
        self.assigned_worker: Optional[User] = None
        self.created_at: datetime = datetime.now()

    def mark_as_resolved(self) -> None:
        "Переводить завдання у статус виконаного."
        self.is_resolved = True


class Project:
    "Сутність проєкту, яка агрегує список завдань."
    
    def __init__(self, project_id: int, project_title: str):
        self.project_id = project_id
        self.project_title = project_title
        self.task_list: List[Task] = []

    def append_new_task(self, task_item: Task) -> None:
        "Додає нове завдання до поточного проєкту."
        if task_item not in self.task_list:
            self.task_list.append(task_item)