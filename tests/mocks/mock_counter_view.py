from app.interface import CounterViewInterface
from app.interface import CounterViewPresenterInterface

class MockCounterView(CounterViewInterface):
    """
    Мок-объект для представления счетчика, используемый в тестах.
    Позволяет проверять состояние UI без отрисовки реальных окон.
    """

    def __init__(self):
        super().__init__()
        # Текущее отображаемое значение счетчика
        self.counter_label: str = "0"
        # Состояние кнопки сброса (включена/выключена)
        self.reset_button_enabled: bool = False
        # Состояние кнопки уменьшения (включена/выключена)
        self.decrement_button_enabled: bool = False
        # Флаг, указывающий, было ли показано подтверждение выхода
        self.exit_confirmation_shown: bool = False
        # Возвращаемое значение для show_exit_confirmation (по умолчанию True)
        self.exit_confirmation_return: bool = True

        self.presenter: CounterViewPresenterInterface = None

    def set_presenter(self, presenter: CounterViewPresenterInterface):
        """
        Устанавливает ссылку на презентер для передачи событий.
        Args:
            presenter: экземпляр презентера счетчика
        """
        self.presenter = presenter

    def update_display(self, value: int) -> None:
        """
        Обновляет отображаемое значение счетчика.
        Args:
            value: новое значение для отображения
        """
        self.counter_label = str(value)

    def set_reset_button_enabled(self, enabled: bool) -> None:
        """
        Включает или выключает кнопку сброса.
        Args:
            enabled: True для включения, False для отключения
        """
        self.reset_button_enabled = enabled

    def set_decrement_button_enabled(self, enabled: bool) -> None:
        """
        Включает или выключает кнопку уменьшения.
        Args:
            enabled: True для включения, False для отключения
        """
        self.decrement_button_enabled = enabled

    def show_exit_confirmation(self) -> bool:
        """
        Имитирует показ диалога подтверждения выхода.
        Returns:
            True, если пользователь подтвердил выход
        """
        self.exit_confirmation_shown = True

        return self.exit_confirmation_return

    def on_increment_click(self, _event):
        """
        Обрабатывает событие клика на кнопку увеличения.
        Args:
            _event: событие клика (не используется)
        """
        if self.presenter:
            self.presenter.handle_increment()

    def on_decrement_click(self, _event):
        """
        Обрабатывает событие клика на кнопку уменьшения.
        Args:
            _event: событие клика (не используется)
        """
        if self.presenter:
            self.presenter.handle_decrement()

    def on_reset_click(self, _event):
        """
        Обрабатывает событие клика на кнопку сброса.
        Args:
            _event: событие клика (не используется)
        """
        if self.presenter:
            self.presenter.handle_reset()

    def on_show_log_click(self, _event):
        """
        Обрабатывает событие клика на кнопку показа истории.
        Args:
            _event: событие клика (не используется)
        """
        if self.presenter:
            self.presenter.handle_show_log()