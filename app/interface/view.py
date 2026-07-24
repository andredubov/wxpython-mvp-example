from abc import abstractmethod
from .presenter import CounterViewPresenterInterface
from .presenter import LogViewPresenterInterface
from .window import WindowInterface


class CounterViewInterface(WindowInterface):
    """
    Интерфейс представления счетчика.

    Расширяет базовый WindowInterface методами,
    специфичными для управления счетчиком.
    """

    @abstractmethod
    def set_presenter(self, presenter: CounterViewPresenterInterface) -> None:
        """
        Устанавливает ссылку на презентер.

        Args:
            presenter: Экземпляр презентера для обработки событий.
        """
        ...

    @abstractmethod
    def update_display(self, value: int) -> None:
        """
        Обновляет отображение значения счетчика.

        Args:
            value: Новое значение для отображения.
        """
        ...

    @abstractmethod
    def set_reset_button_enabled(self, enabled: bool) -> None:
        """
        Включает/выключает кнопку сброса.

        Args:
            enabled: True для включения, False для отключения.
        """
        ...

    @abstractmethod
    def set_decrement_button_enabled(self, enabled: bool) -> None:
        """
        Включает/выключает кнопку уменьшения.

        Args:
            enabled: True для включения, False для отключения.
        """
        ...

    @abstractmethod
    def show_exit_confirmation(self) -> bool:
        """
        Показывает диалог подтверждения выхода.

        Returns:
            bool: True если пользователь подтвердил выход.
        """
        ...


class LogViewInterface(WindowInterface):
    """
    Интерфейс представления логов.

    Расширяет базовый WindowInterface методами для управления логами.
    """

    @abstractmethod
    def set_presenter(self, presenter: LogViewPresenterInterface) -> None:
        """
        Устанавливает ссылку на презентер.

        Args:
            presenter: Экземпляр презентера для обработки событий.
        """
        ...

    @abstractmethod
    def append_log(self, message: str) -> None:
        """
        Добавляет сообщение в лог.

        Args:
            message: Сообщение для добавления.
        """
        ...

    @abstractmethod
    def clear_log(self) -> None:
        """Очищает лог."""
        ...