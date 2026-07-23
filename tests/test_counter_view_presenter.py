import unittest
import logging

from app.model import CounterModel
from app.presenter import CounterViewPresenter
from tests.mocks import MockAppRouter, MockCounterView

class TestCounterViewPresenter(unittest.TestCase):

    def setUp(self):
        """Создаем новую модель перед каждым тестом"""
        # Отключаем логирование для тестов (опционально)
        logging.disable(logging.CRITICAL)

        self.counter_model = CounterModel()
        self.app_router = MockAppRouter()
        self.counter_view = MockCounterView()
        self.counter_view_presenter = CounterViewPresenter(
            model=self.counter_model, 
            view=self.counter_view, 
            router=self.app_router
        )

    def tearDown(self):
        """Восстанавливаем логирование после тестов"""
        logging.disable(logging.NOTSET)

    def test_presenter_handles_increment(self):
        """
        Проверяет, что презентер правильно обрабатывает увеличение счетчика.
        """
        # Проверяем начальное значение
        self.assertEqual(self.counter_model.get_count(), 0)
        self.assertEqual(self.counter_view.counter_label, "0")

        # Вызываем увеличение
        self.counter_view_presenter.handle_increment()

        # Проверяем, что модель обновилась
        self.assertEqual(self.counter_model.get_count(), 1)
        # Проверяем, что представление обновилось
        self.assertEqual(self.counter_view.counter_label, "1")
        # Проверяем, что кнопка сброса стала активной
        self.assertTrue(self.counter_view.reset_button_enabled)
        # Проверяем, что кнопка уменьшения стала активной
        self.assertTrue(self.counter_view.decrement_button_enabled)

    def test_presenter_handles_decrement(self):
        """
        Проверяет, что презентер правильно обрабатывает уменьшение счетчика.
        """
        # Устанавливаем значение счетчика
        self.counter_model.set_count(5)
        self.assertEqual(self.counter_model.get_count(), 5)
        self.assertEqual(self.counter_view.counter_label, "5")

        # Вызываем уменьшение
        self.counter_view_presenter.handle_decrement()

        # Проверяем, что модель обновилась
        self.assertEqual(self.counter_model.get_count(), 4)
        # Проверяем, что представление обновилось
        self.assertEqual(self.counter_view.counter_label, "4")
        # Проверяем, что кнопка сброса активна
        self.assertTrue(self.counter_view.reset_button_enabled)
        # Проверяем, что кнопка уменьшения активна
        self.assertTrue(self.counter_view.decrement_button_enabled)

        # Уменьшаем до нуля
        self.counter_view_presenter.handle_decrement()
        self.counter_view_presenter.handle_decrement()
        self.counter_view_presenter.handle_decrement()
        self.counter_view_presenter.handle_decrement()

        # Проверяем, что модель стала 0
        self.assertEqual(self.counter_model.get_count(), 0)
        # Проверяем, что представление отображает "0"
        self.assertEqual(self.counter_view.counter_label, "0")
        # Проверяем, что кнопка сброса стала неактивной
        self.assertFalse(self.counter_view.reset_button_enabled)
        # Проверяем, что кнопка уменьшения стала неактивной
        self.assertFalse(self.counter_view.decrement_button_enabled)

    def test_presenter_handles_reset(self):
        """
        Проверяет, что презентер правильно обрабатывает сброс счетчика.
        """
        # Устанавливаем значение счетчика
        self.counter_model.set_count(5)
        self.assertEqual(self.counter_model.get_count(), 5)
        self.assertEqual(self.counter_view.counter_label, "5")

        # Вызываем сброс
        self.counter_view_presenter.handle_reset()

        # Проверяем, что модель обновилась
        self.assertEqual(self.counter_model.get_count(), 0)
        # Проверяем, что представление обновилось
        self.assertEqual(self.counter_view.counter_label, "0")
        # Проверяем, что кнопка сброса стала неактивной
        self.assertFalse(self.counter_view.reset_button_enabled)
        # Проверяем, что кнопка уменьшения стала неактивной
        self.assertFalse(self.counter_view.decrement_button_enabled)

    def test_presenter_handles_show_log(self):
        """
        Проверяет, что презентер правильно обрабатывает запрос на показ логов.
        """
        # Проверяем, что метод show_log_window еще не вызывался
        self.assertEqual(self.app_router.show_log_calls, 0)

        # Вызываем показ логов
        self.counter_view_presenter.handle_show_log()

        # Проверяем, что метод show_log_window был вызван один раз
        self.assertEqual(self.app_router.show_log_calls, 1)

    def test_presenter_initial_view_state(self):
        """
        Проверяет, что при инициализации презентер корректно отображает начальное состояние модели.
        """
        # Проверяем, что модель имеет начальное значение 0
        self.assertEqual(self.counter_model.get_count(), 0)
        # Проверяем, что представление отображает "0"
        self.assertEqual(self.counter_view.counter_label, "0")
        # Проверяем, что кнопка сброса неактивна
        self.assertFalse(self.counter_view.reset_button_enabled)
        # Проверяем, что кнопка уменьшения неактивна
        self.assertFalse(self.counter_view.decrement_button_enabled)

    def test_presenter_handles_exit_request(self):
        """
        Проверяет, что презентер правильно обрабатывает запрос на выход из приложения.
        """
        # Подготавливаем мок: подтверждение выхода возвращает True
        self.counter_view.exit_confirmation_return = True

        # Вызываем выход
        self.counter_view_presenter.handle_exit_request()

        # Проверяем, что метод show_exit_confirmation был вызван
        self.assertTrue(self.counter_view.exit_confirmation_shown)
        # Проверяем, что метод close_all был вызван
        self.assertTrue(self.app_router.is_closed_all)

        # Сбрасываем состояние
        self.app_router.is_closed_all = False
        self.counter_view.exit_confirmation_shown = False

        # Подготавливаем мок: подтверждение выхода возвращает False (отмена)
        self.counter_view.exit_confirmation_return = False

        # Вызываем выход
        self.counter_view_presenter.handle_exit_request()

        # Проверяем, что метод show_exit_confirmation был вызван
        self.assertTrue(self.counter_view.exit_confirmation_shown)
        # Проверяем, что метод close_all НЕ был вызван (выход отменён)
        self.assertFalse(self.app_router.is_closed_all)

    def test_presenter_on_model_changed_updates_view(self):
        """
        Проверяет, что метод on_model_changed обновляет представление при изменении модели.
        """
        # Проверяем начальное состояние
        self.assertEqual(self.counter_view.counter_label, "0")
        self.assertFalse(self.counter_view.reset_button_enabled)
        self.assertFalse(self.counter_view.decrement_button_enabled)

        # Вызываем on_model_changed с новым значением
        self.counter_view_presenter.on_model_changed(5, "тест")

        # Проверяем, что представление обновилось
        self.assertEqual(self.counter_view.counter_label, "5")
        self.assertTrue(self.counter_view.reset_button_enabled)
        self.assertTrue(self.counter_view.decrement_button_enabled)

        # Вызываем on_model_changed с нулевым значением
        self.counter_view_presenter.on_model_changed(0, "тест")

        # Проверяем, что кнопки стали неактивными
        self.assertEqual(self.counter_view.counter_label, "0")
        self.assertFalse(self.counter_view.reset_button_enabled)
        self.assertFalse(self.counter_view.decrement_button_enabled)

