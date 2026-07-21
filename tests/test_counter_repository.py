import unittest
import logging
import os

from app.repository import CounterRepository

class TestCounterRepository(unittest.TestCase):
    """Тесты для репозитория счетчика"""

    def setUp(self):
        """Создаем новый репозиторий перед каждым тестом"""
        self.repository = CounterRepository()
        # Отключаем логирование для тестов (опционально)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        """Восстанавливаем логирование после тестов"""
        logging.disable(logging.NOTSET)

    def test_load_value_returns_int(self):
        """Тест загрузки значения счётчика"""
        value = self.repository.load_value()
        self.assertIsInstance(value, int)

    def test_save_and_load_value(self):
        """Тест сохранения и загрузки значения счётчика"""
        test_value = 42
        self.repository.save_value(test_value)
        loaded_value = self.repository.load_value()
        self.assertEqual(loaded_value, test_value)

    def test_load_value_when_file_missing(self):
        """Тест загрузки значения при отсутствующем файле конфигурации"""
        # Сохраняем текущий путь и удаляем файл, если он существует
        config_path = self.repository._config_path
        if os.path.exists(config_path):
            os.remove(config_path)
        
        # При отсутствии файла load_value должен вернуть 0
        value = self.repository.load_value()
        self.assertEqual(value, 0)

    def test_save_value_creates_directory(self):
        """Тест создания директории при сохранении"""
        config_path = self.repository._config_path

        # Если директория существует, удаляем только файл, не директорию
        if os.path.exists(config_path):
            os.remove(config_path)

        # Сохраняем значение — должна создаться директория (если её нет)
        test_value = 100
        self.repository.save_value(test_value)

        # Проверяем, что файл создан и значение записано
        self.assertTrue(os.path.exists(config_path))
        loaded_value = self.repository.load_value()
        self.assertEqual(loaded_value, test_value)