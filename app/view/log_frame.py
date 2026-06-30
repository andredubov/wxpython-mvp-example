import wx
import os
import logging

class LogView(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.logger = logging.getLogger(__name__)
        self.set_window_icon()
        self.init_ui()

    def debug_paths(self):
        """Выводит все возможные пути для отладки"""
        self.logger.info(f"__file__: {__file__}")
        self.logger.info(f"Is compiled by Nuitka: {bool(globals().get('__compiled__'))}")
        self.logger.info(f"Current working dir: {os.getcwd()}")
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        icon_path = os.path.join(project_root, 'assets', 'icons', 'app_icon_16.png')
        self.logger.info(f"Target icon path: {icon_path} - exists: {os.path.exists(icon_path)}")

    def set_window_icon(self):
        """Находит и устанавливает иконку приложения"""
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
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Многострочное текстовое поле только для чтения
        self.log_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

        vbox.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(vbox)

    def append_log(self, message: str):
        """Метод для добавления новой строки лога"""
        self.log_text.AppendText(message + "\n")
