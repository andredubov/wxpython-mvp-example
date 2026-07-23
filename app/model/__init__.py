# Из конкретного файла импортируем класс модели
from .counter_model import CounterModel

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterModel']

__version__ = "1.0.0"
__author__ = "Andrei Dubov"