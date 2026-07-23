# Из конкретного файла импортируем класс
from .counter_presenter import CounterViewPresenter
from .log_presenter import LogViewPresenter

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'CounterViewPresenter',
    'LogViewPresenter',
    ]

__version__ = "1.0.0"
__author__ = "Andrei Dubov"