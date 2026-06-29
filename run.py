import wx

from app.router import AppRouter
from app.model import CounterModel
from app.utils import hide_splash_screen, ensure_hdpi


def InitLocale():
    # Добавляем путь к каталогам с переводами
    wx.Locale.AddCatalogLookupPathPrefix('./app/locales')
    # Создаем и сохраняем объект локали
    locale = wx.Locale()
    # Указываем русский язык (код 1049)
    lang_id = wx.LANGUAGE_RUSSIAN
    # Инициализируем локаль
    if locale.Init(lang_id):
        # Добавляем каталог с переводами
        locale.AddCatalog('app')
        print("Russian locale initialized successfully")
        return True
    else:
        print("Failed to initialize Russian locale, using default")
        return False


def main():
    # 1. Инициализируем графическое приложение wxPython
    app = wx.App(False)

    # 2. Локализуем графическое приложение wxPython
    InitLocale()

    # 3. Создание общей модели данных
    model = CounterModel()

    # 4. Создаем роутер и передаем ему управление навигацией
    router = AppRouter(model)
    router.start()
    hide_splash_screen()
    
    # 5. Запускаем главный бесконечный цикл приложения
    app.MainLoop()


if __name__ == '__main__':
    ensure_hdpi()
    main()