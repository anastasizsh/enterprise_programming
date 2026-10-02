import unittest
from domain.entities import User, Task, Project
from application.use_cases import CreateTask, AssignTask, CompleteTask

class TestTaskManagementSystem(unittest.TestCase):
    def setUp(self) -> None:
        """Ініціалізація базових даних для кожного тесту."""
        self.test_user = User(user_id=1, full_name="Анастасія", email_address="anastasiia@university.edu")
        self.test_project = Project(project_id=10, project_title="Python ПЗ-1")
        
        self.create_task = CreateTask()
        self.assign_task = AssignTask()
        self.complete_task = CompleteTask()

    def test_create_task_flow(self) -> None:
        """Перевірка створення завдання та додавання його в проєкт."""
        task = self.create_task.execute(
            target_project=self.test_project,
            task_id=101,
            headline="Написати доменний шар",
            details="Створити класи User, Task, Project"
        )
        self.assertEqual(task.task_id, 101)
        self.assertIn(task, self.test_project.task_list)
        self.assertFalse(task.is_resolved)

    def test_assign_task_flow(self) -> None:
        """Перевірка прив'язки користувача до завдання."""
        task = Task(task_id=102, headline="Тест", details="Деталі")
        self.assign_task.execute(target_task=task, worker=self.test_user)
        self.assertEqual(task.assigned_worker, self.test_user)

    def test_assign_resolved_task_raises_error(self) -> None:
        """Перевірка захисту від призначення закритого завдання."""
        task = Task(task_id=103, headline="Тест 2", details="Деталі 2")
        task.mark_as_resolved()
        
        with self.assertRaises(ValueError):
            self.assign_task.execute(target_task=task, worker=self.test_user)

    def test_complete_task_flow(self) -> None:
        """Перевірка успішного закриття завдання."""
        task = Task(task_id=104, headline="Здати роботу", details="Завантажити в систему")
        self.complete_task.execute(target_task=task)
        self.assertTrue(task.is_resolved)

if __name__ == "__main__":
    unittest.main()