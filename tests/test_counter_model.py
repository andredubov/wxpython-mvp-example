import unittest
from app.model import CounterModel


class TestCounterModel(unittest.TestCase):
    """Простой тест для модели счетчика"""

    def setUp(self):
        """Создаем новую модель перед каждым тестом"""
        self.model = CounterModel(initial_value=0)

    def test_initial_value(self):
        """Тест: проверяем начальное значение"""
        self.assertEqual(self.model.get_count(), 0)
        # Проверяем с другим начальным значением
        model2 = CounterModel(initial_value=10)
        self.assertEqual(model2.get_count(), 10)

    def test_increment(self):
        """Тест: проверяем увеличение счетчика"""
        self.model.increment()
        self.assertEqual(self.model.get_count(), 1)
        self.model.increment()
        self.assertEqual(self.model.get_count(), 2)

    def test_decrement(self):
        """Тест: проверяем уменьшение счетчика"""
        self.model.set_count(5)
        self.model.decrement()
        self.assertEqual(self.model.get_count(), 4)
        self.model.decrement()
        self.assertEqual(self.model.get_count(), 3)

    def test_decrement_cannot_go_negative(self):
        """Тест: decrement() не должен уходить в минус"""
        self.assertEqual(self.model.get_count(), 0)
        self.model.decrement()
        self.assertEqual(self.model.get_count(), 0)
        self.model.set_count(1)
        self.model.decrement()
        self.assertEqual(self.model.get_count(), 0)
        self.model.decrement()
        self.assertEqual(self.model.get_count(), 0)

    def test_set_count(self):
        """Тест: проверяем установку значения"""
        self.model.set_count(42)
        self.assertEqual(self.model.get_count(), 42)
        self.model.set_count(100)
        self.assertEqual(self.model.get_count(), 100)

    def test_set_count_cannot_go_negative(self):
        """Тест: set_count() не должен устанавливать отрицательное значение"""
        self.model.set_count(-5)
        self.assertEqual(self.model.get_count(), 0)
        self.model.set_count(-10)
        self.assertEqual(self.model.get_count(), 0)

    def test_reset(self):
        """Тест: проверяем сброс счетчика"""
        self.model.set_count(10)
        self.assertEqual(self.model.get_count(), 10)
        self.model.reset()
        self.assertEqual(self.model.get_count(), 0)
        self.model.set_count(25)
        self.model.reset()
        self.assertEqual(self.model.get_count(), 0)
        """
        Тест: Проверяем, что уведомления отправляются с правильным описанием действия
        """
        actions = []
        def callback(value, action):
            actions.append(action)
        self.model.subscribe(callback)
        # Проверяем разные действия
        self.model.increment()
        self.assertEqual(actions[0], "увеличение (+1)")
        self.model.decrement()
        self.assertEqual(actions[1], "уменьшение (-1)")
        self.model.reset()
        self.assertEqual(actions[2], "сброс (0)")
        self.model.set_count(42)
        self.assertEqual(actions[3], "установка значения из ссылки (42)")

    def test_subscribers_receive_notifications(self):
        """Тест: проверяем уведомления подписчиков"""
        notifications = []
        def callback(value, action):
            notifications.append((value, action))
        # Подписываемся
        self.model.subscribe(callback)
        # Выполняем операции
        self.model.increment()          # (1, "увеличение (+1)")
        self.model.set_count(5)         # (5, "установка значения из ссылки (5)")
        self.model.decrement()          # (4, "уменьшение (-1)")
        self.model.reset()              # (0, "сброс (0)")
        # Проверяем все уведомления
        expected = [
            (1, "увеличение (+1)"),
            (5, "установка значения из ссылки (5)"),
            (4, "уменьшение (-1)"),
            (0, "сброс (0)")
        ]
        self.assertEqual(notifications, expected)


if __name__ == '__main__':
    unittest.main()