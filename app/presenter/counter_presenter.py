from app.interface import AppRouterInterface
from app.interface import CounterViewInterface
from app.interface import CounterModelInterface
from app.interface import CounterViewPresenterInterface


class CounterViewPresenter(CounterViewPresenterInterface):
    """
    Презентер для управления счетчиком.

    Реализует бизнес-логику приложения, связывая модель данных
    с представлением. Обрабатывает команды пользователя и обновляет
    интерфейс при изменении состояния модели.
    """

    def __init__(self, model: CounterModelInterface, view: CounterViewInterface, router: AppRouterInterface):
        """
        Инициализирует презентер.

        Args:
            model: Модель данных счетчика.
            view: Представление (главное окно).
            router: Маршрутизатор для навигации между окнами.
        """
        self.model = model
        self.view = view
        self.router = router

        self.view.set_presenter(self)
        
        # Подписываемся на модель
        self.model.subscribe(self.on_model_changed)
        
        # Первичное отображение
        self.on_model_changed(new_value=self.model.get_count(), action=None)

    def handle_increment(self):
        """
        Обрабатывает запрос на увеличение счетчика.

        Вызывается при клике на кнопку "+".
        """
        self.model.increment()

    def handle_decrement(self):
        """
        Обрабатывает запрос на уменьшение счетчика.

        Вызывается при клике на кнопку "-".
        """
        self.model.decrement()

    def handle_reset(self):
        """
        Обрабатывает запрос на сброс счетчика.

        Вызывается при клике на кнопку "Сброс".
        """
        self.model.reset()

    def handle_show_log(self):
        """
        Обрабатывает запрос на открытие окна логов.

        Вызывается при клике на кнопку "Показать историю".
        """
        self.router.show_log_window()

    def handle_exit_request(self):
        """
        Обрабатывает запрос на выход из приложения.

        Показывает диалог подтверждения выхода. При согласии пользователя
        закрывает все окна через маршрутизатор.
        """
        if self.view.show_exit_confirmation():
            self.router.close_all()

    def on_model_changed(self, new_value: int, action: str):
        # 1. Обновляем текстовое поле счетчика
        self.view.update_display(new_value)

        # 2. Управляем доступностью кнопки: активна, только если значение не 0
        is_not_zero = (new_value != 0)
        self.view.set_reset_button_enabled(is_not_zero)
        self.view.set_decrement_button_enabled(is_not_zero)