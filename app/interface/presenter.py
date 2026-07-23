from abc import ABC, abstractmethod

class CounterViewPresenterInterface(ABC):
    """Интерфейс презентера счетчика"""

    @abstractmethod
    def handle_increment(self) -> None:
        """Обрабатывает нажатие кнопки увеличения"""
        ...

    @abstractmethod
    def handle_decrement(self) -> None:
        """Обрабатывает нажатие кнопки уменьшения"""
        ...

    @abstractmethod
    def handle_reset(self) -> None:
        """Обрабатывает нажатие кнопки сброса"""
        ...

    @abstractmethod
    def handle_show_log(self) -> None:
        """Обрабатывает запрос на показ логов"""
        ...

    @abstractmethod
    def handle_exit_request(self) -> None:
        """Обрабатывает запрос на выход из приложения"""
        ...

    @abstractmethod
    def on_model_changed(self, new_value: int, action: str) -> None:
        """Обрабатывает изменение модели"""
        ...


class LogViewPresenterInterface(ABC):
    """Интерфейс презентера логов"""

    @abstractmethod
    def on_model_changed(self, new_value: int, action: str) -> None:
        """Обрабатывает изменение модели"""
        ...

    @abstractmethod
    def detach(self) -> None:
        """Отписывается от модели при уничтожении"""
        ...