import wx
import os
import logging

class CounterView(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.logger = logging.getLogger(__name__)
        # Ссылка на презентер (будет установлена извне)
        self.presenter = None
        self.set_window_icon()
        self.init_ui()
        
    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Элементы интерфейса
        self.label = wx.StaticText(panel, label="0", style=wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTER_HORIZONTAL)
        font = self.label.GetFont()
        font.SetPointSize(20)
        self.label.SetFont(font)
        
        self.btn_inc = wx.Button(panel, label="+")
        self.btn_dec = wx.Button(panel, label="-")
        self.btn_reset = wx.Button(panel, label="Сброс")
        self.btn_show_log = wx.Button(panel, label="Показать историю")
        
        # Компоновка
        vbox.Add(self.label, 1, wx.EXPAND | wx.TOP, 20)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_dec, 1, wx.EXPAND | wx.ALL, 5)
        hbox.Add(self.btn_inc, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(hbox, 1, wx.EXPAND)
        vbox.Add(self.btn_reset, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        vbox.Add(self.btn_show_log, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        panel.SetSizer(vbox)
        
        # Привязка событий GUI к методам презентера
        self.btn_inc.Bind(wx.EVT_BUTTON, self.on_increment_click)
        self.btn_dec.Bind(wx.EVT_BUTTON, self.on_decrement_click)
        self.btn_reset.Bind(wx.EVT_BUTTON, self.on_reset_click)
        self.btn_show_log.Bind(wx.EVT_BUTTON, self.on_show_log_click)
        
        self.Centre()

    def set_window_icon(self):
        """Находит и устанавливает иконку приложения"""
        try:
            # Вычисляем путь к app/assets/icons/app_icon.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir) # папка app
            icon_path = os.path.join(project_root, 'assets', 'icons', 'app-icon.png')
            
            if os.path.exists(icon_path):
                # Создаем wx.Icon из PNG файла
                icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
                self.SetIcon(icon)
        except Exception as e:
            # Если иконка не загрузилась, приложение продолжит работу со стандартной иконкой ОС
            self.logger.error(f"Не удалось загрузить иконку: {e}")

    def set_presenter(self, presenter):
        self.presenter = presenter

    def update_display(self, value):
        """Метод для изменения текста на экране"""
        self.label.SetLabel(str(value))

    def on_increment_click(self, event):
        if self.presenter:
            self.presenter.handle_increment()

    def on_decrement_click(self, event):
        if self.presenter:
            self.presenter.handle_decrement()

    def on_reset_click(self, event):
        if self.presenter:
            self.presenter.handle_reset()

    def on_show_log_click(self, event):
        if self.presenter:
            self.presenter.handle_show_log()

    def show_exit_confirmation(self) -> bool:
        """
        Показывает диалоговое окно подтверждения выхода.
        Возвращает True, если пользователь подтвердил выход, иначе False.
        """
        dialog = wx.MessageDialog(
            self,
            message="Вы действительно хотите выйти из приложения?",
            caption="Подтверждение выхода",
            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
        )
        
        # Выводим диалог на экран (он блокирует остальной интерфейс)
        result = dialog.ShowModal()
        dialog.Destroy() # Обязательно освобождаем ресурсы диалога
        
        # Если нажата кнопка "Да" (wx.ID_YES), возвращаем True
        return result == wx.ID_YES