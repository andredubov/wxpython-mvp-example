import wx

from app.router import AppRouter
from app.model import CounterModel

def main():
    # 1. Инициализируем графическое приложение wxPython
    app = wx.App(False)

    # 2. Создание общей модели данных
    model = CounterModel()

    # 3. Создаем роутер и передаем ему управление навигацией
    router = AppRouter(model)
    router.start()
    
    # 4. Запускаем главный бесконечный цикл приложения
    app.MainLoop()


if __name__ == '__main__':
    main()