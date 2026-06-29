import wx
import logging

from logging.handlers import RotatingFileHandler
from app.utils import ensure_hdpi

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
    handlers=[
        RotatingFileHandler(
            './application.log',
            maxBytes=5*1024*1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

class MyApplication(wx.App):
    def __init__(self):
        self.locale = None
        self.logger = logging.getLogger(__name__)
        super().__init__(redirect=False)

    def OnInit(self):
        try:
            ensure_hdpi()
            self.InitLocale()
            self.logger.info("Application initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Initialization error: {e}")
            return False

    def InitLocale(self):
        if self.locale is not None:
            return True
        # Добавляем путь к каталогам с переводами
        wx.Locale.AddCatalogLookupPathPrefix('./locales')
        # Создаем и сохраняем объект локали
        self.locale = wx.Locale()
        # Указываем русский язык (код 1049)
        lang_id = wx.LANGUAGE_RUSSIAN
        # Инициализируем локаль
        if self.locale.Init(lang_id):
            # Добавляем каталог с переводами
            self.locale.AddCatalog('app')
            self.logger.info("Russian locale initialized successfully")
            return True
        else:
            self.logger.warning("Failed to initialize Russian locale, using default")
            return False