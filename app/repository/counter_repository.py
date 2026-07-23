import os
import sys
import json
import logging

from app.interface.repository import CounterRepositoryInterface


class CounterRepository(CounterRepositoryInterface):
    """
    Репозиторий для хранения значения счетчика в JSON-файле.

    Реализует сохранение и загрузку числа в файл config.json.
    Путь к файлу определяется автоматически в зависимости от
    способа запуска (разработка или скомпилированный бинарник).
    """

    def __init__(self):
        """
        Инициализирует репозиторий и определяет путь к конфигурационному файлу.

        При сборке в один исполняемый файл (Nuitka) использует директорию
        запускаемого файла, иначе — папку assets в проекте.
        """
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
        """
        Загружает сохраненное значение счетчика из файла конфигурации.

        Returns:
            int: Загруженное значение или 0, если файл не существует
                 или произошла ошибка при чтении.
        """
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("last_value", 0)
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке значения из репозитория: {e}")
        return 0

    def save_value(self, value: int):
        """
        Сохраняет значение счетчика в файл конфигурации.

        Создает недостающие директории в пути к файлу, если они отсутствуют.

        Args:
            value (int): Значение счетчика для сохранения.
        """
        try:
            dir_name = os.path.dirname(self._config_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            data = {"last_value": value}
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении значения в репозиторий: {e}")