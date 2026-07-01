import os
import sys
import json
import logging

class CounterRepository:
    """
    Инфраструктурный слой (Repository).
    Отвечает исключительно за сохранение и загрузку данных с жесткого диска.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Надежное определение путей
        if globals().get('__compiled__'):
            executable_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            self._config_path = os.path.join(executable_dir, 'config.json')
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)  # папка app
            self._config_path = os.path.join(project_root, 'assets', 'config.json')

        self.logger.info(f"Репозиторий инициализирован. Путь к конфигу: {self._config_path}")

    def load_value(self) -> int:
        """Считывает сохраненное значение счетчика из файла"""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("last_value", 0)
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке значения из репозитория: {e}")
        return 0

    def save_value(self, value: int):
        """Записывает переданное значение счетчика в JSON-файл"""
        try:
            dir_name = os.path.dirname(self._config_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            data = {"last_value": value}
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении значения в репозиторий: {e}")