# Из конкретного файла импортируем класс
from .mock_counter_repository import MockCounterRepository
from .mock_counter_view import MockCounterView
from .mock_router import MockAppRouter

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'MockCounterRepository',
    'MockAppRouter',
    'MockCounterView',
    ]
__version__ = "1.0.0"