# Из конкретного файла импортируем класс модели
from .counter_model import CounterModel

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterModel']