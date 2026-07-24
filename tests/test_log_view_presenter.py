import unittest
import logging

from app.model import CounterModel
from app.presenter import LogViewPresenter
from tests.mocks import MockLogView


class TestLogViewPresenter(unittest.TestCase):
    """
    Тесты для презентера логов.

    Проверяет, что LogViewPresenter правильно подписывается на модель,
    добавляет записи в лог при изменениях и корректно отписывается.
    """

    def setUp(self):
        """Создаем новую модель и презентер перед каждым тестом"""
        logging.disable(logging.CRITICAL)

        self.counter_model = CounterModel(initial_value=5)
        self.log_view = MockLogView()
        self.log_presenter = LogViewPresenter(
            model=self.counter_model,
            view=self.log_view
        )

    def tearDown(self):
        """Восстанавливаем логирование после тестов"""
        logging.disable(logging.NOTSET)

    def test_presenter_initial_log_entry(self):
        """
        Проверяет, что при инициализации презентера в лог добавляется
        начальное сообщение с текущим значением счетчика.
        """
        expected_message = f"Приложение запущено. Начальное значение: 5"
        self.assertIn(expected_message, self.log_view.log_messages)
        self.assertEqual(len(self.log_view.log_messages), 1)

    def test_presenter_subscribes_to_model(self):
        """
        Проверяет, что презентер подписывается на модель при создании.
        """
        # Проверяем, что презентер подписан на модель
        self.assertIn(
            self.log_presenter.callback,
            self.counter_model._listeners
        )

    def test_presenter_appends_log_on_model_change(self):
        """
        Проверяет, что при изменении модели в лог добавляется
        соответствующее сообщение.
        """
        # Начальное состояние: 1 запись (приветственное сообщение)
        initial_count = len(self.log_view.log_messages)

        # Изменяем модель
        self.counter_model.increment()

        # Проверяем, что в лог добавилась запись
        self.assertEqual(len(self.log_view.log_messages), initial_count + 1)
        expected_message = "Действие: увеличение (+1) -> Новое значение: 6"
        self.assertEqual(self.log_view.log_messages[-1], expected_message)

    def test_presenter_appends_correct_messages_for_all_actions(self):
        """
        Проверяет, что для всех типов действий в лог записываются
        правильные сообщения.
        """
        # Сброс счетчика
        self.counter_model.reset()
        self.assertEqual(
            self.log_view.log_messages[-1],
            "Действие: сброс (0) -> Новое значение: 0"
        )

        # Установка значения
        self.counter_model.set_count(10)
        self.assertEqual(
            self.log_view.log_messages[-1],
            "Действие: установка значения из ссылки (10) -> Новое значение: 10"
        )

        # Уменьшение
        self.counter_model.decrement()
        self.assertEqual(
            self.log_view.log_messages[-1],
            "Действие: уменьшение (-1) -> Новое значение: 9"
        )

    def test_presenter_detach_unsubscribes_from_model(self):
        """
        Проверяет, что метод detach() отписывает презентер от модели.
        """
        # Проверяем, что презентер подписан
        self.assertIn(
            self.log_presenter.callback,
            self.counter_model._listeners
        )

        # Отписываемся
        self.log_presenter.detach()

        # Проверяем, что подписка удалена
        self.assertNotIn(
            self.log_presenter.callback,
            self.counter_model._listeners
        )

    def test_presenter_stops_receiving_updates_after_detach(self):
        """
        Проверяет, что после detach() презентер больше не получает
        уведомлений об изменениях модели.
        """
        # Запоминаем количество сообщений до отписки
        messages_before = len(self.log_view.log_messages)

        # Отписываемся
        self.log_presenter.detach()

        # Изменяем модель
        self.counter_model.increment()
        self.counter_model.increment()

        # Проверяем, что новых сообщений не появилось
        self.assertEqual(len(self.log_view.log_messages), messages_before)

    def test_presenter_multiple_log_entries(self):
        """
        Проверяет, что при нескольких изменениях модели в лог
        добавляются все соответствующие записи.
        """
        # Выполняем несколько операций
        self.counter_model.increment()
        self.counter_model.increment()
        self.counter_model.decrement()
        self.counter_model.reset()
        self.counter_model.set_count(7)

        # Проверяем количество записей
        # 1 начальная + 5 операций = 6 записей
        self.assertEqual(len(self.log_view.log_messages), 6)

        # Проверяем последнюю запись
        self.assertEqual(
            self.log_view.log_messages[-1],
            "Действие: установка значения из ссылки (7) -> Новое значение: 7"
        )


if __name__ == '__main__':
    unittest.main()