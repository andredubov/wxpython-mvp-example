import unittest
import logging

from app.router import AppRouter
from app.model import CounterModel
from tests.mocks import MockCounterRepository
from tests.mocks import MockWindowFactory

class TestRouter(unittest.TestCase):
    """Тесты для представления счетчика"""

    def setUp(self):
        """Создаем новую модель перед каждым тестом"""
        self.window_factory = MockWindowFactory()
        self.counter_model = CounterModel()
        self.counter_repository = MockCounterRepository()
        self.router = AppRouter(model=self.counter_model, repository=self.counter_repository, window_factory=self.window_factory)
        # Отключаем логирование для тестов (опционально)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        """Восстанавливаем логирование после тестов"""
        logging.disable(logging.NOTSET)

    def test_router_initialization(self):
        """
        Проверяет, что роутер правильно инициализируется с моделью и репозиторием.
        """
        # Проверяем, что роутер создан с правильными зависимостями
        self.assertIsNotNone(self.router)
        self.assertEqual(self.router.model, self.counter_model)
        self.assertEqual(self.router.repository, self.counter_repository)

        # Проверяем, что главное окно и окно логов изначально не созданы
        self.assertIsNone(self.router.main_view)
        self.assertIsNone(self.router.main_view_presenter)
        self.assertIsNone(self.router.log_view)
        self.assertIsNone(self.router.log_view_presenter)

    def test_show_log_window_creates_log_view(self):
        """
        Проверяет, что метод show_log_window создает окно логов.
        """
        # Проверяем, что изначально лог не создан
        self.assertIsNone(self.router.log_view)
        self.assertIsNone(self.router.log_view_presenter)

        # Создаем главное окно, чтобы можно было открыть лог
        self.router.start()
        self.assertIsNotNone(self.router.main_view)

        # Открываем окно логов
        self.router.show_log_window()

        # Проверяем, что окно логов и презентер созданы
        self.assertIsNotNone(self.router.log_view)
        self.assertIsNotNone(self.router.log_view_presenter)
    
        