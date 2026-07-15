import logging

from app.interface.model import CounterModelInterface


class CounterModel(CounterModelInterface):
    """
    Класс Модели.
    Отвечает исключительно за хранение данных счетчика
    и выполнение математических операций над ними.
    """
    def __init__(self, initial_value: int = 0):
        self.logger = logging.getLogger(__name__)
        self._count = initial_value
        self._listeners = []  # Список колбэков для уведомления

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
        if self._count > 0:
            self._count -= 1
            self._notify("уменьшение (-1)")
        else:
            self.logger.warning("Попытка уменьшить счетчик ниже нуля заблокирована.")

    def reset(self):
        """Сбрасывает значение счетчика на 0"""
        self._count = 0
        self._notify("сброс (0)")

    def set_count(self, value: int):
        if value < 0:
            value = 0
        self._count = value
        self._notify(f"установка значения из ссылки ({value})")

    def get_count(self) -> int:
        """Возвращает текущее значение счетчика"""
        return self._count