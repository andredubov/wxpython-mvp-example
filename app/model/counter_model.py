import json
import os
import logging

class CounterModel:
    """
    Класс Модели.
    Отвечает исключительно за хранение данных счетчика
    и выполнение математических операций над ними.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._count = 0
        self._listeners = []  # Список колбэков для уведомления

        # Определяем путь к файлу конфигурации
        # app/models/counter_model.py -> app/assets/config.json
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._config_path = os.path.join(base_dir, 'assets', 'config.json')
        
        # Загружаем сохраненное значение при старте
        self.load_from_file()

    def subscribe(self, callback):
        """Регистрация презентера на обновления модели"""
        self._listeners.append(callback)
    
    def unsubscribe(self, callback):
        """Удаляет презентер из списка уведомлений"""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify(self, action: str):
        """Уведомление всех подписчиков об изменении"""
        for callback in self._listeners:
            callback(self._count, action)

    def increment(self):
        """Увеличивает значение счетчика на 1"""
        self._count += 1
        self._notify("увеличение (+1)")

    def decrement(self):
        """Уменьшает значение счетчика на 1"""
        self._count -= 1
        self._notify("уменьшение (-1)")

    def reset(self):
        """Сбрасывает значение счетчика на 0"""
        self._count = 0
        self._notify("сброс (0)")

    def get_count(self) -> int:
        """Возвращает текущее значение счетчика"""
        return self._count
    
    def load_from_file(self):
        """Загружает значение счетчика из файла конфигурации"""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._count = data.get("last_value", 0)
        except Exception:
            # Если файл поврежден или недоступен, стартуем с нуля
            self._count = 0

    def save_to_file(self):
        """Сохраняет текущее значение счетчика в JSON-файл"""
        try:
            # Убедимся, что папка assets существует
            os.makedirs(os.path.dirname(self._config_path), exist_ok=True)
            
            data = {"last_value": self._count}
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении файла: {e}")
            
