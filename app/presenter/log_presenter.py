class LogViewPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Сохраняем ссылку на метод, чтобы потом точно его удалить
        self.callback = self.on_model_changed

        # Подписываемся на обновления модели
        self.model.subscribe(self.on_model_changed)
        
        # Начальная запись
        self.view.append_log(f"Приложение запущено. Начальное значение: {self.model.get_count()}")

    def detach(self):
        """Вызывается при уничтожении окна для предотвращения утечки памяти"""
        self.model.unsubscribe(self.callback)

    def on_model_changed(self, new_value: int, action: str):
        """Вызывается автоматически, когда модель меняет состояние"""
        log_message = f"Действие: {action} -> Новое значение: {new_value}"
        self.view.append_log(log_message)
