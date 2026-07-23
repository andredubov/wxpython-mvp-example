import os

from app.interface import CounterRepositoryInterface

class MockCounterRepository(CounterRepositoryInterface):
    """
    Мок-репозиторий для тестирования.
    
    Используется в unit-тестах для эмуляции работы с хранилищем данных.
    В отличие от реального репозитория, данные хранятся только в памяти
    и не сохраняются на диск, что позволяет изолировать тесты.
    
    Attributes:
        counter_value (int): Текущее значение счетчика, хранящееся в памяти.
    """

    def __init__(self):
        """
        Инициализация мок-репозитория.
        
        Устанавливает начальное значение счетчика равным 0.
        """
        self.counter_value = 0

    def load_value(self) -> int:
        """
        Загружает сохраненное значение счетчика.
        
        Returns:
            int: Текущее значение счетчика, хранящееся в памяти.
        """
        return self.counter_value

    def save_value(self, value: int) -> None:
        """
        Сохраняет значение счетчика в память.
        
        В отличие от реального репозитория, этот метод не записывает
        данные в файл, а только обновляет поле counter_value.
        
        Args:
            value (int): Значение, которое будет сохранено.
        """
        self.counter_value = value