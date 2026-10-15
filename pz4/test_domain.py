import unittest
import uuid
from datetime import date, timedelta
from todo_app.domain.models import Task, TaskStatus, Priority, Deadline
from todo_app.domain.services import TaskPriorityCalculator

class TestDomainLogic(unittest.TestCase):
    def setUp(self):
        self.project_id = uuid.uuid4()
        self.today = date.today()

    def test_task_creation_generates_uuid(self):
        task = Task(title="Написати звіт", project_id=self.project_id)
        self.assertIsInstance(task.id, uuid.UUID)
        self.assertEqual(task.status, TaskStatus.NEW)

    def test_task_start(self):
        task = Task(title="Кодити", project_id=self.project_id)
        task.start()
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

    def test_task_complete(self):
        task = Task(title="Зробити ПЗ", project_id=self.project_id)
        task.complete()
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    def test_is_overdue(self):
        past_date = self.today - timedelta(days=2)
        task = Task(title="Запізнення", project_id=self.project_id, deadline=Deadline(past_date))
        self.assertTrue(task.is_overdue(self.today))

    def test_is_not_overdue_if_completed(self):
        past_date = self.today - timedelta(days=2)
        task = Task(title="Вчасно здано", project_id=self.project_id, deadline=Deadline(past_date))
        task.complete()
        self.assertFalse(task.is_overdue(self.today))

    def test_priority_calculator_high(self):
        close_deadline = self.today + timedelta(days=2)
        task = Task(title="Терміново", project_id=self.project_id, deadline=Deadline(close_deadline))
        calculated = TaskPriorityCalculator.calculate_urgency(task, self.today)
        self.assertEqual(calculated, Priority.HIGH)

if __name__ == "__main__":
    unittest.main()