import unittest
from unittest.mock import Mock

# Импортируем тестируемые классы
from app.model import CounterModel
from app.presenter import CounterPresenter

class TestCounterPresenter(unittest.TestCase):
    def setUp(self):
        """
        Этот метод выполняется ПЕРЕД каждым тестом.
        Здесь мы создаем чистое окружение для теста.
        """
        # 1. Создаем реальную модель
        self.model = CounterModel()
        
        # 2. Создаем Mock вместо реального графического окна (View).
        # Нам не важен интерфейс wxPython, важен лишь факт вызова его методов.
        self.mock_view = Mock()
        
        # 3. Инициализируем тестируемый презентер
        self.presenter = CounterPresenter(self.model, self.mock_view)


    def test_initialization_sets_presenter_and_updates_view(self):
        """Проверяем, что при старте презентер связывает себя с view и обновляет экран"""
        # Проверяем, вызвал ли презентер метод set_presenter у окна
        self.mock_view.set_presenter.assert_called_once_with(self.presenter)
        
        # Проверяем, отобразилось ли начальное значение (0) на экране
        self.mock_view.update_display.assert_called_with(0)


    def test_handle_reset_logic(self):
        """Тест логики сброса (Reset)"""
        # Искусственно меняем состояние модели (имитируем, что пользователь уже нащелкал до 5)
        self.model._count = 5
        
        # Сбрасываем историю вызовов mock-объекта, чтобы очистить вызовы из setUp
        self.mock_view.reset_mock()
        
        # Вызываем тестируемый метод презентера (как будто нажали кнопку Сброс)
        self.presenter.handle_reset()
        
        # ПРОВЕРКА 1: Проверяем, что значение в модели действительно обнулилось
        self.assertEqual(self.model.get_count(), 0)
        
        # ПРОВЕРКА 2: Проверяем, что презентер дал команду View обновить интерфейс
        # и передал туда новое значение (0)
        self.mock_view.update_display.assert_called_once_with(0)


    def test_handle_increment_updates_model_and_view(self):
        """Тест метода инкремента (кнопка +)"""
        # Сбрасываем историю вызовов mock-объекта из setUp
        self.mock_view.reset_mock()
        
        # Нажимаем "+" в первый раз
        self.presenter.handle_increment()
        
        # ПРОВЕРКА: Значение в модели стало 1, а представление обновилось
        self.assertEqual(self.model.get_count(), 1)
        self.mock_view.update_display.assert_called_once_with(1)
        
        # Нажимаем "+" во второй раз
        self.mock_view.reset_mock()
        self.presenter.handle_increment()
        
        # ПРОВЕРКА: Значение стало 2, представление снова обновилось
        self.assertEqual(self.model.get_count(), 2)
        self.mock_view.update_display.assert_called_once_with(2)


    def test_handle_decrement_updates_model_and_view(self):
        """Тест метода декремента (кнопка -)"""
        # Искусственно выставим начальное значение в 10
        self.model._count = 10
        self.mock_view.reset_mock()
        
        # Нажимаем "-" 
        self.presenter.handle_decrement()
        
        # ПРОВЕРКА: Значение упало до 9, представление получило команду отобразить 9
        self.assertEqual(self.model.get_count(), 9)
        self.mock_view.update_display.assert_called_once_with(9)


if __name__ == '__main__':
    unittest.main()
