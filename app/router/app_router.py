import wx

from app.view import CounterView, LogView
from app.presenter import CounterPresenter, LogPresenter
from app.utils import hide_splash_screen

class AppRouter:
    """
    Сущность Навигации (Router).
    Отвечает за создание, открытие и координацию окон.
    """
    def __init__(self, model):
        self.model = model
        self.main_view = None
        self.main_presenter = None
        self.log_view = None
        self.log_presenter = None

    def start(self):
        """Открывает главное окно приложения"""
        if not self.main_view:
            self.main_view = CounterView(parent=None, title="Управление счетчиком")
            main_view_size = (450, 250)
            self.main_view.SetSize(main_view_size)
            self.main_view.SetMinSize(main_view_size)
            self.main_view.Center()
            # Передаем роутер в презентер, если главному окну нужно будет открыть лог
            self.main_presenter = CounterPresenter(model=self.model, view=self.main_view, router=self)

            # Перехватываем попытку закрытия главного окна (нажатие на крестик)
            self.main_view.Bind(wx.EVT_CLOSE, self._on_main_window_close_request)

        self.main_view.Show()

    def hide_splash_screen(self):
        hide_splash_screen()

    def show_log_window(self):
        """Открывает окно логов (или выводит на передний план, если открыто)"""
        if not self.log_view:
            self.log_view = LogView(parent=self.main_view, title="История изменений (Лог)")
            self.log_presenter = LogPresenter(self.model, self.log_view)

            # Позиционируем рядом с главным окном
            if self.main_view:
                main_view_position = self.main_view.GetPosition()
                main_view_size = self.main_view.GetSize()
                new_position_x = main_view_position.x + main_view_size.width
                self.log_view.SetPosition((new_position_x, main_view_position.y))
                log_view_size = (500, 250)
                self.log_view.SetSize(log_view_size)
                self.log_view.SetMinSize(log_view_size)

            # При закрытии окна логов зануляем ссылку, чтобы его можно было открыть снова
            self.log_view.Bind(wx.EVT_CLOSE, self._on_log_window_close)
            self.log_view.Show()
        else:
            self.log_view.Raise() # Выводим на передний план, если уже открыто

    def close_all(self):
        """Уничтожает все окна приложения и освобождает ресурсы"""
        # Сохраняем данные в файл
        if self.model:
            self.model.save_to_file()
        # Сначала отписываем и закрываем лог (если он открыт), чтобы избежать утечки памяти
        if self.log_presenter:
            self.log_presenter.detach()
            self.log_presenter = None
        if self.log_view:
            self.log_view.Destroy() # Используем Destroy вместо Close, чтобы обойти проверки
            self.log_view = None
        # Теперь уничтожаем главное окно
        if self.main_view:
            self.main_view.Destroy()
            self.main_view = None

    def _on_log_window_close(self, event):
        """Вызывается, когда пользователь закрывает окно логов крестиком"""
        if self.log_presenter:
            self.log_presenter.detach()
            self.log_presenter = None

        self.log_view = None
        event.Skip()

    def _on_main_window_close_request(self, event):
        """Вызывается при попытке закрыть главное окно"""
        # Делегируем логику презентеру, у которого есть доступ к диалогу подтверждения
        if self.main_presenter:
            self.main_presenter.handle_exit_request()

        # Внимание: мы НЕ вызываем event.Skip(), поэтому окно не закроется само по себе,
        # пока Роутер не вызовет метод close_all()