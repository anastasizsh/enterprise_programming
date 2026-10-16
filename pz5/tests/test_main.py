import unittest
from domain.models import Task, TaskStatus
from application.use_cases import AssignTaskUseCase
from infrastructure.senders import EmailSender

class FakeRepository:
    def __init__(self):
        self.saved_tasks = []
        
    def save(self, task):
        self.saved_tasks.append(task)

class TestTaskManagementSystem(unittest.TestCase):
    def test_assign_task_use_case(self):
        repo = FakeRepository()
        notifier = EmailSender()
        use_case = AssignTaskUseCase(repo, notifier)
        
        task = Task(title="Зібрати проєкт")
        use_case.execute(task, user_id=999)
        
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
        self.assertEqual(task.assignee_id, 999)
        self.assertIn(task, repo.saved_tasks)

if __name__ == '__main__':
    unittest.main()