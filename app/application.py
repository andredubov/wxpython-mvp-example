import wx
import logging

from logging.handlers import RotatingFileHandler
from app.utils import ensure_hdpi
from app.router import AppRouter
from app.model import CounterModel
from app.repository import CounterRepository
from app.factory import DefaultWindowFactory

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
        self.router = None
        self.model = None
        self.repository = None
        self.locale = None
        self.logger = logging.getLogger(__name__)
        super().__init__(redirect=False)

    def OnInit(self):
        try:
            # 1. Включаем поддержку High-DPI для Windows
            ensure_hdpi()
            self.logger.info("Поддержка High-DPI включена")

            # 2. Инициализируем локализацию (русский язык)
            self.InitLocale()

            # 3. Создаем репозиторий и загружаем сохраненные данные
            self.repository = CounterRepository()
            initial_value = self.repository.load_value()
            self.logger.info(f"Загружено начальное значение: {initial_value}")

            # 4. Создаем модель с загруженным значением
            self.model = CounterModel(initial_value=initial_value)

            self.window_factory = DefaultWindowFactory()

            # 5. Создаем роутер и запускаем приложение
            self.router = AppRouter(model=self.model, repository=self.repository, window_factory=self.window_factory)
            self.router.start()

            # 6. Если есть сплэш-скрин - скрываем его
            self.router.hide_splash_screen()

            # 7. Регистрируем обработчики завершения сессии Windows
            self.Bind(wx.EVT_QUERY_END_SESSION, self.OnQueryEndSession)
            self.Bind(wx.EVT_END_SESSION, self.OnEndSession)

            self.logger.info("Приложение успешно инициализировано")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка инициализации: {e}", exc_info=True)
            # Гарантируем, что модель и репозиторий существуют (как None)
            self.model = None
            self.repository = None
            # Показываем сообщение об ошибке пользователю
            wx.MessageBox(f"Ошибка инициализации приложения:\n{str(e)}", "Критическая ошибка",
                wx.OK | wx.ICON_ERROR
            )
            return False

    def OnExit(self):
        """
        Вызывается при выходе из приложения.
        Сохраняет данные и освобождает ресурсы.
        """
        self.logger.info("Завершение работы приложения...")

        if self.repository and self.model:
            try:
                current_value = self.model.get_count()
                self.repository.save_value(current_value)
                self.logger.info(f"Данные сохранены: значение={current_value}")
            except Exception as e:
                self.logger.error(f"Ошибка при сохранении данных: {e}")

        return super().OnExit()

    def OnQueryEndSession(self, event):
        """
        Вызывается при завершении сессии Windows.
        """
        self.logger.info("Завершение сессии Windows, сохранение данных...")

        if self.repository and self.model:
            try:
                current_value = self.model.get_count()
                self.repository.save_value(current_value)
                self.logger.info(f"Данные сохранены при завершении сессии: значение={current_value}")
            except Exception as e:
                self.logger.error(f"Ошибка при сохранении данных: {e}")

        event.Skip()

    def OnEndSession(self, event):
        """
        Вызывается при завершении сессии Windows (альтернативный обработчик).
        """
        self.logger.info("Получено событие завершения сессии Windows")

        if self.repository and self.model:
            try:
                current_value = self.model.get_count()
                self.repository.save_value(current_value)
                self.logger.info(f"Данные сохранены при завершении сессии: значение={current_value}")
            except Exception as e:
                self.logger.error(f"Ошибка при сохранении данных: {e}")

        event.Skip()

    def InitLocale(self):
        """
        Инициализация локализации для поддержки русского языка.
        """
        if self.locale is not None:
            return True

        try:
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
                self.logger.info("Русская локализация инициализирована")
                return True
            else:
                self.logger.warning("Не удалось инициализировать русскую локализацию, используется язык по умолчанию")
                return False
        except Exception as e:
            self.logger.error(f"Ошибка инициализации локализации: {e}")
            return False