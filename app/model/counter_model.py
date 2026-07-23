import logging

from app.interface.model import CounterModelInterface


class CounterModel(CounterModelInterface):
    """
    Модель данных счетчика с поддержкой подписки на изменения.

    Хранит текущее значение счетчика и позволяет увеличивать,
    уменьшать и сбрасывать его. Поддерживает механизм наблюдателя
    (Observer) для уведомления подписанных слушателей.
    """

    def __init__(self, initial_value: int = 0):
        """
        Инициализирует модель счетчика.

        Args:
            initial_value (int): Начальное значение счетчика. По умолчанию 0.
        """
        self.logger = logging.getLogger(__name__)
        self._count = initial_value
        self._listeners = []  # Список колбэков для уведомления

    def subscribe(self, callback):
        """
        Подписывает слушателя на уведомления об изменениях.

        Args:
            callback: Функция, вызываемая при изменении счетчика.
                     Принимает два аргумента: (new_value, action).
        """
        self._listeners.append(callback)

    def unsubscribe(self, callback):
        """
        Отписывает слушателя от уведомлений.

        Args:
            callback: Функция, которая была передана в subscribe().
        """
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify(self, action: str):
        """
        Уведомляет всех подписанных слушателей об изменении состояния.

        Args:
            action (str): Описание выполненного действия.
        """
        for callback in self._listeners:
            callback(self._count, action)

    def increment(self):
        """
        Увеличивает значение счетчика на 1.
        Уведомляет подписанных слушателей.
        """
        self._count += 1
        self._notify("увеличение (+1)")

    def decrement(self):
        """
        Уменьшает значение счетчика на 1, если текущее значение > 0.
        При попытке уменьшить ниже нуля логирует предупреждение.
        Уведомляет подписанных слушателей при успешном изменении.
        """
        if self._count > 0:
            self._count -= 1
            self._notify("уменьшение (-1)")
        else:
            self.logger.warning("Попытка уменьшить счетчик ниже нуля заблокирована.")

    def reset(self):
        """
        Сбрасывает значение счетчика на 0.
        Уведомляет подписанных слушателей.
        """
        self._count = 0
        self._notify("сброс (0)")

    def set_count(self, value: int):
        """
        Устанавливает значение счетчика.
        При отрицательном значении устанавливает 0.
        Уведомляет подписанных слушателей.

        Args:
            value (int): Новое значение счетчика.
        """
        if value < 0:
            value = 0
        self._count = value
        self._notify(f"установка значения из ссылки ({value})")

    def get_count(self) -> int:
        """
        Возвращает текущее значение счетчика.

        Returns:
            int: Текущее значение счетчика.
        """
        return self._count