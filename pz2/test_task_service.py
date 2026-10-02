import unittest
from unittest.mock import MagicMock
from models import User
from services import NotificationSender, TaskService


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.mock_notifier = MagicMock(spec=NotificationSender)
        self.service = TaskService(notifier=self.mock_notifier)
        self.user = User(
            id=1,
            name="Anastasiia",
            email="anastasiia@example.com",
            phone="+380991112233"
        )

    def test_create_task_with_assignee(self):
        task = self.service.create_task(
            title="Setup repository",
            description="Init structure",
            assignee=self.user
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Setup repository")
        self.assertEqual(len(self.service.get_tasks()), 1)
        self.mock_notifier.send.assert_called_once()

    def test_create_task_without_assignee(self):
        task = self.service.create_task(title="Refactor service", description="Clean up")

        self.assertEqual(task.title, "Refactor service")
        self.mock_notifier.send.assert_not_called()

    def test_create_task_empty_title_raises_error(self):
        with self.assertRaises(ValueError):
            self.service.create_task(title="   ", description="Empty")

        self.mock_notifier.send.assert_not_called()


if __name__ == "__main__":
    unittest.main()