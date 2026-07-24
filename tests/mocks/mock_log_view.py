from app.interface import LogViewInterface
from app.interface import LogViewPresenterInterface

class MockLogView(LogViewInterface):

    def __init__(self):
        super().__init__()
        self.log_messages = []
        self.presenter: LogViewPresenterInterface = None

    def set_presenter(self, presenter: LogViewPresenterInterface):
        """
        Устанавливает ссылку на презентер для передачи событий.
        Args:
            presenter: экземпляр презентера счетчика
        """
        self.presenter = presenter

    def append_log(self, message: str) -> None:
        """
        Добавляет сообщение в лог.

        Args:
            message: Сообщение для добавления.
        """
        self.log_messages.append(message)

    def clear_log(self) -> None:
        """Очищает лог."""
        self.log_messages.clear()