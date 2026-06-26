# Из конкретного файла импортируем класс презентора
from .counter_presenter import CounterPresenter
from .log_presenter import LogPresenter

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterPresenter','LogPresenter']