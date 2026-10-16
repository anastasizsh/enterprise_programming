from datetime import date
from .models import Task, Priority, TaskStatus

class TaskPriorityCalculator:
    @staticmethod
    def calculate_urgency(task: Task, current_date: date) -> Priority:
        if not task.deadline or task.status == TaskStatus.COMPLETED:
            return task.priority
            
        days_left = (task.deadline.due_date - current_date).days
        if days_left <= 3:
            return Priority.HIGH
        elif days_left <= 7:
            return Priority.MEDIUM
        return Priority.LOW