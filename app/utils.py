"""
Вспомогательные утилиты для приложения.

Содержит служебные функции для настройки DPI, управления
заставкой при сборке Nuitka и другие вспомогательные задачи.
"""


def hide_splash_screen():
    """
    Удаляет временный файл заставки при сборке в один файл (Nuitka).

    Используется для корректного закрытия окна заставки при запуске
    скомпилированного приложения.
    """
    import tempfile, os
    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(tempfile.gettempdir(), "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]))
        if os.path.exists(splash_filename):
            os.unlink(splash_filename)


def ensure_hdpi():
    """
    Включает поддержку высокого DPI (HiDPI) для приложения на Windows.

    Использует соответствующий API в зависимости от версии операционной системы:
    - Windows 7: SetProcessDPIAware (старый API)
    - Windows 8.1+: SetProcessDpiAwareness (новый API)

    В случае ошибки настройки DPI продолжает работу без изменений.
    """
    import platform, ctypes, sys
    
    if platform.system() == "Windows":
        try:
            # Проверяем версию Windows
            version = sys.getwindowsversion()

            # Для Windows 7 и старше используем старый API
            if version.major == 6 and version.minor == 1:  # Windows 7
                try:
                    # Старый API для Windows 7
                    ctypes.windll.user32.SetProcessDPIAware()
                except Exception:
                    pass  # Игнорируем ошибки на Windows 7
            else:
                # Для Windows 8.1+ используем новый API
                try:
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
                except AttributeError:
                    try:
                        # Fallback для Windows Vista+
                        ctypes.windll.user32.SetProcessDPIAware()
                    except AttributeError:
                        pass  # Старые версии Windows без DPI поддержки
        except Exception:
            # Если любая проверка fails, просто игнорируем DPI настройки
            pass