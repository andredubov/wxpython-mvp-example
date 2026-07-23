import wx
import os
import logging

from app.interface.view import LogViewInterface
from app.view.base_wx_view import WxViewMixin

class LogView(wx.Frame, LogViewInterface, WxViewMixin):
    """
    Окно для отображения логов в формате текстового поля.

    Наследует wx.Frame для создания GUI, LogViewInterface для
    контракта представления и WxViewMixin для вспомогательных методов.
    """

    def __init__(self, parent: wx.Window, title: str):
        """
        Инициализация окна логов.

        Args:
            parent: Родительское окно (wx.Window).
            title: Заголовок окна (str).
        """
        super().__init__(parent, title=title)
        self.logger = logging.getLogger(__name__)
        self.set_window_icon()
        self.init_ui()

    def debug_paths(self):
        """
        Логирование отладочной информации о путях к файлам.

        Используется для диагностики проблем с поиском иконок
        и других ресурсов.
        """
        self.logger.info(f"__file__: {__file__}")
        self.logger.info(f"Is compiled by Nuitka: {bool(globals().get('__compiled__'))}")
        self.logger.info(f"Current working dir: {os.getcwd()}")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        icon_path = os.path.join(project_root, 'assets', 'icons', 'app_icon_16.png')
        self.logger.info(f"Target icon path: {icon_path} - exists: {os.path.exists(icon_path)}")

    def set_window_icon(self):
        """
        Установка иконки для окна.

        Ищет файл иконки в папке assets/icons/app_icon_16.png.
        В случае ошибки загрузки продолжает работу со стандартной иконкой.
        """
        try:
            self.debug_paths()
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

    def init_ui(self):
        """
        Инициализация пользовательского интерфейса.

        Создает панель и размещает в ней многострочное текстовое поле
        для отображения логов.
        """
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Многострочное текстовое поле только для чтения
        self.log_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(vbox)

    def append_log(self, message: str):
        """
        Добавляет новую строку в окно логов.

        Args:
            message (str): Текст сообщения для добавления.
        """
        self.log_text.AppendText(message + "\n")