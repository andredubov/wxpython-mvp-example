from abc import ABC, abstractmethod


class RepositoryInterface(ABC):
    """Интерфейс репозитория для работы с данными"""

    @abstractmethod
    def load_value(self) -> int:
        """Загружает сохраненное значение счетчика"""
        ...

    @abstractmethod
    def save_value(self, value: int) -> None:
        """Сохраняет значение счетчика"""
        ...