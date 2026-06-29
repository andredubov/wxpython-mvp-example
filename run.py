from app import MyApplication
from app.router import AppRouter
from app.model import CounterModel

def main():
    # 1. Инициализируем графическое приложение wxPython
    app = MyApplication()

    # 3. Создание общей модели данных
    model = CounterModel()

    # 4. Создаем роутер и передаем ему управление навигацией
    router = AppRouter(model)
    router.start()
    router.hide_splash_screen()
    
    # 5. Запускаем главный бесконечный цикл приложения
    app.MainLoop()

if __name__ == '__main__':
    main()