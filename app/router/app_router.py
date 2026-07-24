from app.presenter import CounterViewPresenter, LogViewPresenter
from app.interface import CounterRepositoryInterface, CounterModelInterface
from app.interface import AppRouterInterface, WindowFactoryInterface
from app.factory import DefaultWindowFactory
from app.utils import hide_splash_screen


class AppRouter(AppRouterInterface):
    """
    Маршрутизатор приложения, управляющий окнами и их жизненным циклом.

    Реализует интерфейс AppRouterInterface. Отвечает за:
    - Создание и отображение главного окна и окна логов.
    - Связывание представлений с соответствующими презентерами.
    - Управление закрытием окон с сохранением данных.
    """

    def __init__(self, model: CounterModelInterface, repository: CounterRepositoryInterface, window_factory: WindowFactoryInterface = None):
        """
        Инициализирует маршрутизатор.

        Args:
            model: Модель данных счетчика.
            repository: Репозиторий для сохранения/загрузки данных.
            window_factory: Фабрика для создания окон. Если не указана,
                           используется DefaultWindowFactory.
        """
        self.model = model
        self.repository = repository
        self.window_factory = window_factory or DefaultWindowFactory()
        self.main_view = None
        self.main_view_presenter = None
        self.log_view = None
        self.log_view_presenter = None

    def start(self):
        """
        Создает и отображает главное окно приложения.

        При первом вызове создает экземпляр главного окна,
        настраивает его размер и позицию, связывает с презентером.
        """
        if not self.main_view:
            self.main_view = self.window_factory.create_counter_view(parent=None, title="Управление счетчиком")
            main_view_size = (450, 250)
            self.main_view.set_size(main_view_size)
            self.main_view.set_min_size(main_view_size)
            self.main_view.center()
            # Передаем роутер в презентер, если главному окну нужно будет открыть лог
            self.main_view_presenter = CounterViewPresenter(model=self.model, view=self.main_view, router=self)

            # Перехватываем попытку закрытия главного окна (нажатие на крестик)
            self.main_view.bind_close(self._on_main_window_close_request)

        self.main_view.show()

    def hide_splash_screen(self):
        """
        Удаляет файл заставки при сборке в один исполняемый файл (Nuitka).

        Вызывается после инициализации приложения для корректного
        закрытия окна заставки.
        """
        hide_splash_screen()

    def show_log_window(self):
        """
        Открывает окно логов или выводит его на передний план, если уже открыто.

        При первом открытии создает окно логов, связывает с презентером,
        позиционирует справа от главного окна и настраивает обработку закрытия.
        """
        if not self.log_view:
            self.log_view = self.window_factory.create_log_view(parent=self.main_view, title="История изменений (Лог)")
            self.log_view_presenter = LogViewPresenter(self.model, self.log_view)

            # Позиционируем рядом с главным окном
            if self.main_view:
                main_view_position = self.main_view.get_position()
                main_view_size = self.main_view.get_size()
                new_position_x = main_view_position.x + main_view_size.width
                self.log_view.set_position((new_position_x, main_view_position.y))
                log_view_size = (500, 250)
                self.log_view.set_size(log_view_size)
                self.log_view.set_min_size(log_view_size)

            # При закрытии окна логов зануляем ссылку, чтобы его можно было открыть снова
            self.log_view.bind_close(self._on_log_window_close)
            self.log_view.show()
        else:
            self.log_view.raise_on_top() # Выводим на передний план, если уже открыто

    def close_all(self):
        """
        Закрывает все окна приложения и сохраняет текущие данные.

        Порядок закрытия:
        1. Сохраняет текущее значение счетчика через репозиторий.
        2. Отсоединяет презентер логов и уничтожает окно логов.
        3. Уничтожает главное окно.
        """
        # Сохраняем данные через репозиторий, забирая текущее число из модели
        if self.repository and self.model:
            current_value = self.model.get_count()
            self.repository.save_value(current_value)

        # Сначала отписываем и закрываем лог (если он открыт), чтобы избежать утечки памяти
        if self.log_view_presenter:
            self.log_view_presenter.detach()
            self.log_view_presenter = None
        if self.log_view:
            self.log_view.destroy() # Используем Destroy вместо Close, чтобы обойти проверки
            self.log_view = None
        # Теперь уничтожаем главное окно
        if self.main_view:
            self.main_view.destroy()
            self.main_view = None

    def _on_log_window_close(self, event):
        """
        Обработчик закрытия окна логов.

        Отсоединяет презентер и уничтожает окно, освобождая ресурсы.
        """
        if self.log_view_presenter:
            self.log_view_presenter.detach()
            self.log_view_presenter = None

        if self.log_view:
            self.log_view.destroy()
            self.log_view = None

    def _on_main_window_close_request(self, event):
        """
        Обработчик запроса на закрытие главного окна.

        Делегирует обработку презентеру главного окна, который показывает
        диалог подтверждения выхода. Окно не закрывается автоматически —
        это должно быть выполнено через close_all().

        Args:
            event: Событие закрытия окна (wx.EVT_CLOSE).
        """
        # Делегируем логику презентеру, у которого есть доступ к диалогу подтверждения
        if self.main_view_presenter:
            self.main_view_presenter.handle_exit_request()

        # Внимание: мы НЕ вызываем event.Skip(), поэтому окно не закроется само по себе,
        # пока Роутер не вызовет метод close_all()