import unittest
import uuid
from application.use_cases import CreateTaskUseCase, CompleteTaskUseCase, CompleteProjectUseCase, CreateTaskDTO, CompleteTaskDTO, CompleteProjectDTO, ErrorCode
from infrastructure.repositories import InMemoryTaskRepository
from infrastructure.senders import EmailSender
from domain.models import Task

class TestApplicationLayer(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryTaskRepository()
        self.notifier = EmailSender()

    def test_create_task_success(self):
        use_case = CreateTaskUseCase(self.repo)
        result = use_case.execute(CreateTaskDTO(title="Нове завдання"))
        
        self.assertTrue(result.is_success)
        self.assertEqual(result.data.title, "Нове завдання")

    def test_complete_task_success(self):
        create_uc = CreateTaskUseCase(self.repo)
        task_result = create_uc.execute(CreateTaskDTO(title="Завдання 1"))
        
        complete_uc = CompleteTaskUseCase(self.repo, self.notifier)
        result = complete_uc.execute(CompleteTaskDTO(task_id=task_result.data.id))
        
        self.assertTrue(result.is_success)
        self.assertEqual(result.data.status, "completed")

    def test_complete_task_not_found(self):
        use_case = CompleteTaskUseCase(self.repo, self.notifier)
        result = use_case.execute(CompleteTaskDTO(task_id=uuid.uuid4()))
        
        self.assertFalse(result.is_success)
        self.assertEqual(result.error, ErrorCode.NOT_FOUND)

    def test_transactional_rollback(self):
        project_id = uuid.uuid4()
        
        task1 = Task(title="Нормальне завдання", project_id=project_id)
        task2 = Task(title="Зламати транзакцію", project_id=project_id)
        self.repo.save(task1)
        self.repo.save(task2)
        
        use_case = CompleteProjectUseCase(self.repo)
        result = use_case.execute(CompleteProjectDTO(project_id=project_id))
        
        self.assertFalse(result.is_success)
        
        checked_task = self.repo.get_by_id(task1.id)
        self.assertEqual(checked_task.status.value, "new")

if __name__ == '__main__':
    unittest.main()