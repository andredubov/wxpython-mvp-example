# Из конкретного файла импортируем класс
from .mock_counter_repository import MockCounterRepository
from .mock_counter_view import MockCounterView
from .mock_log_view import MockLogView
from .mock_router import MockAppRouter
from .mock_window_factory import MockWindowFactory

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'MockWindowFactory',
    'MockCounterRepository',
    'MockAppRouter',
    'MockCounterView',
    'MockLogView',
    ]
__version__ = "1.0.0"