import wx
import os
import logging

class LogView(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.logger = logging.getLogger(__name__)
        self.set_window_icon()
        self.init_ui()

    def set_window_icon(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            icon_path = os.path.join(project_root, 'assets', 'icons', 'app-icon.png')

            if os.path.exists(icon_path):
                icon = wx.Icon(icon_path, wx.BITMAP_TYPE_PNG)
                self.SetIcon(icon)
        except Exception as e:
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
