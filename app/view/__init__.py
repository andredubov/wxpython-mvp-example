# Из конкретного файла импортируем класс модели
from .main_frame import CounterView
from .log_frame import LogView

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterView','LogView']

__version__ = "1.0.0"