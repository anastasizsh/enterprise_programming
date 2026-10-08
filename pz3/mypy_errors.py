from domain_types import TaskId, UserId
from task_system import create_task, assign_task, Task

task1 = create_task(1, "Написати звіт")
task1.status = "review"
assign_task(task1, "user_123")