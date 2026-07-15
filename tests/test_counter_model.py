import unittest
from app.model import CounterModel


class TestCounterModel(unittest.TestCase):
    """Простой тест для модели счетчика"""

    def setUp(self):
        """Создаем новую модель перед каждым тестом"""
        self.model = CounterModel(initial_value=0)

    def test_increment_increases_count_by_one(self):
        """
        Тест: Проверяем, что метод increment() увеличивает счетчик на 1
        """
        # Начальное значение
        self.assertEqual(self.model.get_count(), 0)

        # Увеличиваем счетчик
        self.model.increment()

        # Проверяем, что значение стало 1
        self.assertEqual(self.model.get_count(), 1)

        # Увеличиваем еще раз
        self.model.increment()

        # Проверяем, что значение стало 2
        self.assertEqual(self.model.get_count(), 2)


if __name__ == '__main__':
    unittest.main()