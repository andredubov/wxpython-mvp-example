import unittest
import logging

from app.model import CounterModel
from app.presenter import CounterViewPresenter
from tests.mocks import MockCounterView, MockAppRouter

class TestCounterView(unittest.TestCase):

    def setUp(self):
        """Создаем новую модель перед каждым тестом"""
        # Отключаем логирование для тестов (опционально)
        logging.disable(logging.CRITICAL)

        self.counter_model = CounterModel()
        self.counter_view = MockCounterView()
        self.app_router = MockAppRouter()
        self.counter_view_presenter = CounterViewPresenter(
            model= self.counter_model, 
            view=self.counter_view,
            router= self.app_router
        )

    def tearDown(self):
        """Восстанавливаем логирование после тестов"""
        logging.disable(logging.NOTSET)

    def test_view_initial_state(self):
        """
        Проверяет, что представление инициализируется с правильным начальным состоянием.
        """
        self.assertEqual(self.counter_view.counter_label, "0")
        self.assertFalse(self.counter_view.reset_button_enabled)
        self.assertFalse(self.counter_view.decrement_button_enabled)
        self.assertFalse(self.counter_view.exit_confirmation_shown)

    def test_view_update_display(self):
        """
        Проверяет, что метод update_display обновляет отображение.
        """
        self.counter_view.update_display(5)
        self.assertEqual(self.counter_view.counter_label, "5")

        self.counter_view.update_display(0)
        self.assertEqual(self.counter_view.counter_label, "0")

    def test_view_set_reset_button_enabled(self):
        """
        Проверяет, что метод set_reset_button_enabled управляет состоянием кнопки сброса.
        """
        self.counter_view.set_reset_button_enabled(True)
        self.assertTrue(self.counter_view.reset_button_enabled)

        self.counter_view.set_reset_button_enabled(False)
        self.assertFalse(self.counter_view.reset_button_enabled)

    def test_view_set_decrement_button_enabled(self):
        """
        Проверяет, что метод set_decrement_button_enabled управляет состоянием кнопки уменьшения.
        """
        self.counter_view.set_decrement_button_enabled(True)
        self.assertTrue(self.counter_view.decrement_button_enabled)

        self.counter_view.set_decrement_button_enabled(False)
        self.assertFalse(self.counter_view.decrement_button_enabled)

    def test_view_show_exit_confirmation(self):
        """
        Проверяет, что метод show_exit_confirmation возвращает правильное значение и устанавливает флаг.
        """
        # Проверяем возврат значения по умолчанию (True)
        result = self.counter_view.show_exit_confirmation()
        self.assertTrue(result)
        self.assertTrue(self.counter_view.exit_confirmation_shown)

        # Сбрасываем состояние
        self.counter_view.exit_confirmation_shown = False
        self.counter_view.exit_confirmation_return = False

        # Проверяем возврат False
        result = self.counter_view.show_exit_confirmation()
        self.assertFalse(result)
        self.assertTrue(self.counter_view.exit_confirmation_shown)

    def test_view_on_increment_click(self):
        """
        Проверяет, что метод on_increment_click вызывает handle_increment у презентера.
        """
        # Создаем мок-презентер
        mock_presenter = self.counter_view_presenter
        mock_presenter.handle_increment = lambda: setattr(mock_presenter, 'increment_called', True)
        mock_presenter.increment_called = False

        # Устанавливаем презентер в представление
        self.counter_view.set_presenter(mock_presenter)

        # Вызываем метод
        self.counter_view.on_increment_click(None)

        # Проверяем, что метод презентера был вызван
        self.assertTrue(mock_presenter.increment_called)

    def test_view_on_decrement_click(self):
        """
        Проверяет, что метод on_decrement_click вызывает handle_decrement у презентера.
        """
        # Создаем мок-презентер
        mock_presenter = self.counter_view_presenter
        mock_presenter.handle_decrement = lambda: setattr(mock_presenter, 'decrement_called', True)
        mock_presenter.decrement_called = False

        # Устанавливаем презентер в представление
        self.counter_view.set_presenter(mock_presenter)

        # Вызываем метод
        self.counter_view.on_decrement_click(None)

        # Проверяем, что метод презентера был вызван
        self.assertTrue(mock_presenter.decrement_called)

    def test_view_on_reset_click(self):
        """
        Проверяет, что метод on_reset_click вызывает handle_reset у презентера.
        """
        # Создаем мок-презентер
        mock_presenter = self.counter_view_presenter
        mock_presenter.handle_reset = lambda: setattr(mock_presenter, 'reset_called', True)
        mock_presenter.reset_called = False

        # Устанавливаем презентер в представление
        self.counter_view.set_presenter(mock_presenter)

        # Вызываем метод
        self.counter_view.on_reset_click(None)

        # Проверяем, что метод презентера был вызван
        self.assertTrue(mock_presenter.reset_called)

    def test_view_on_show_log_click(self):
        """
        Проверяет, что метод on_show_log_click вызывает handle_show_log у презентера.
        """
        # Создаем мок-презентер
        mock_presenter = self.counter_view_presenter
        mock_presenter.handle_show_log = lambda: setattr(mock_presenter, 'show_log_called', True)
        mock_presenter.show_log_called = False

        # Устанавливаем презентер в представление
        self.counter_view.set_presenter(mock_presenter)

        # Вызываем метод
        self.counter_view.on_show_log_click(None)

        # Проверяем, что метод презентера был вызван
        self.assertTrue(mock_presenter.show_log_called)