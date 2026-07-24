import wx
import os
import logging

from app.interface.view import CounterViewInterface
from app.interface.presenter import CounterViewPresenterInterface
from app.view.base_wx_view import WxViewMixin

class CounterView(wx.Frame, CounterViewInterface, WxViewMixin):
    """
    Главное окно приложения для управления счетчиком.

    Наследует wx.Frame для создания GUI, CounterViewInterface для
    контракта представления и WxViewMixin для вспомогательных методов.
    """

    def __init__(self, parent: wx.Window, title: str):
        """
        Инициализирует главное окно приложения.

        Args:
            parent: родительское окно (wx.Window).
            title: заголовок окна (str).
        """
        super().__init__(parent, title=title)
        self.logger = logging.getLogger(__name__)
        # Ссылка на презентер (будет установлена извне)
        self.presenter = None
        self.set_window_icon()
        self.init_ui()

    def init_ui(self):
        """
        Инициализирует пользовательский интерфейс главного окна.
        Создает все виджеты и устанавливает их компоновку.
        """
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

    def debug_paths(self):
        """
        Выводит в лог информацию о путях для отладки.
        Полезно при поиске проблем с загрузкой ресурсов.
        """
        self.logger.info(f"__file__: {__file__}")
        self.logger.info(f"Is compiled by Nuitka: {bool(globals().get('__compiled__'))}")
        self.logger.info(f"Current working dir: {os.getcwd()}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        icon_path = os.path.join(project_root, 'assets', 'icons', 'app_icon_16.png')
        self.logger.info(f"Target icon path: {icon_path} - exists: {os.path.exists(icon_path)}")

    def set_size(self, size):
        super().SetSize(size)

    def center(self):
        super().Center()

    def bind_close(self, handler):
        super().Bind(wx.EVT_CLOSE, handler)

    def destroy(self):
        super().Destroy()

    def set_size(self, size: tuple) -> None:
        super().SetSize(size)

    def set_min_size(self, size: tuple) -> None:
        super().SetMinSize(size)

    def center(self) -> None:
        super().Center()

    def show(self) -> None:
        super().Show()

    def raise_on_top(self) -> None:
        super().Raise()

    def get_position(self) -> tuple:
        return super().GetPosition()

    def get_size(self) -> tuple:
        return super().GetSize()

    def set_window_icon(self):
        """
        Находит и устанавливает иконку окна приложения.
        Иконка загружается из файла app/assets/icons/app_icon_16.png.
        В случае ошибки продолжает работу со стандартной иконкой.
        """
        try:
            # Вычисляем путь к app/assets/icons/app-icon.png
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir) # папка app
            icon_path = os.path.join(project_root, 'assets', 'icons', 'app_icon_16.png')

            if os.path.exists(icon_path):
                # Создаем wx.Icon из PNG файла
                icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
                self.SetIcon(icon)
        except Exception as e:
            # Если иконка не загрузилась, приложение продолжит работу со стандартной иконкой ОС
            self.logger.error(f"Не удалось загрузить иконку: {e}")

    def set_presenter(self, presenter: CounterViewPresenterInterface):
        """
        Устанавливает ссылку на презентер для обработки событий.
        Args:
            presenter: экземпляр презентера счетчика
        """
        self.presenter = presenter

    def update_display(self, value):
        """
        Обновляет отображение значения счетчика.
        Args:
            value: новое значение для отображения
        """
        self.label.SetLabel(str(value))

    def set_reset_button_enabled(self, enabled: bool):
        """
        Включает или выключает кнопку сброса.
        Args:
            enabled: True для включения, False для отключения
        """
        self.btn_reset.Enable(enabled)

    def set_decrement_button_enabled(self, enabled: bool):
        """
        Включает или выключает кнопку уменьшения.
        Args:
            enabled: True для включения, False для отключения
        """
        self.btn_dec.Enable(enabled)

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

    def on_increment_click(self, event):
        """
        Обрабатывает событие клика на кнопку увеличения.
        Args:
            event: событие клика
        """
        if self.presenter:
            self.presenter.handle_increment()

    def on_decrement_click(self, event):
        """
        Обрабатывает событие клика на кнопку уменьшения.
        Args:
            event: событие клика
        """
        if self.presenter:
            self.presenter.handle_decrement()

    def on_reset_click(self, event):
        """
        Обрабатывает событие клика на кнопку сброса.
        Args:
            event: событие клика
        """
        if self.presenter:
            self.presenter.handle_reset()

    def on_show_log_click(self, event):
        """
        Обрабатывает событие клика на кнопку показа истории изменений.
        Args:
            event: событие клика
        """
        if self.presenter:
            self.presenter.handle_show_log()