from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    phone: str


@dataclass
class Task:
    id: int
    title: str
    description: str
    assignee: Optional[User] = None
    status: str = "New"


@dataclass
class Project:
    id: int
    name: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)