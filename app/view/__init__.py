# Из конкретного файла импортируем класс модели
from .main_frame import CounterView
from .log_frame import LogView
from .base_wx_view import WxViewMixin

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterView','LogView','WxViewMixin']
__version__ = "1.0.0"