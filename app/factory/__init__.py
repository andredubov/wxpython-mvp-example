# Из конкретного файла импортируем класс модели
from .window_factory import DefaultWindowFactory

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'DefaultWindowFactory'
]
__version__ = "1.0.0"
__author__ = "Andrei Dubov"