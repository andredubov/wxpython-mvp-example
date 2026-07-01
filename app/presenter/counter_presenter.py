class CounterPresenter:
    def __init__(self, model, view, router):
        self.model = model
        self.view = view
        self.router = router

        self.view.set_presenter(self)
        
        # Подписываемся на модель
        self.model.subscribe(self.on_model_changed)
        
        # Первичное отображение
        self.on_model_changed(new_value=self.model.get_count(), action=None)

    def handle_increment(self):
        """Вызывается при нажатии кнопки '+' в интерфейсе"""
        self.model.increment()

    def handle_decrement(self):
        """Вызывается при нажатии кнопки '-' в интерфейсе"""
        self.model.decrement()
    
    def handle_reset(self):
        """Вызывается при нажатии кнопки Сброс в интерфейсе"""
        self.model.reset()

    def handle_show_log(self):
        """Презентер не создает окно сам, он просит об этом Роутер"""
        self.router.show_log_window()

    def handle_exit_request(self):
        """Проверяет подтверждение выхода и инициирует закрытие через роутер"""
        if self.view.show_exit_confirmation():
            self.router.close_all()

    def on_model_changed(self, new_value: int, action: str):
        """Обновляем UI при изменении данных в модели"""
        # 1. Обновляем текстовое поле счетчика
        self.view.update_display(new_value)

        # 2. Управляем доступностью кнопки: активна, только если значение не 0
        is_not_zero = (new_value != 0)
        self.view.set_reset_button_enabled(is_not_zero)
        self.view.set_decrement_button_enabled(is_not_zero)