# Из конкретного файла импортируем интерфейсы
from .model import CounterModelInterface
from .view import CounterViewInterface, LogViewInterface
from .presenter import CounterViewPresenterInterface, LogViewPresenterInterface
from .repository import CounterRepositoryInterface
from .router import AppRouterInterface
from .factory import WindowFactoryInterface
from .window import WindowInterface

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'CounterModelInterface', 
    'CounterViewInterface',
    'CounterViewPresenterInterface',
    'LogViewInterface',
    'LogViewPresenterInterface',
    'CounterRepositoryInterface',
    'AppRouterInterface',
    'WindowFactoryInterface',
    'WindowInterface',
    ]

__version__ = "1.0.0"
__author__ = "Andrei Dubov"

