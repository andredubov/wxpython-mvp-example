class CounterPresenter:
    def __init__(self, model, view, router):
        self.model = model
        self.view = view
        self.router = router

        self.view.set_presenter(self)
        
        # Подписываемся на модель
        self.model.subscribe(self.on_model_changed)
        
        # Первичное отображение
        self.view.update_display(self.model.get_count())

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
        self.view.update_display(new_value)
