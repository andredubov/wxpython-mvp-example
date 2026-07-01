from app import MyApplication
from app.router import AppRouter
from app.model import CounterModel
from app.repository import CounterRepository

def main():
    # 1. Инициализируем приложение wxPython c графическим пользовательским интерфейсом
    app = MyApplication()

    # 2. Создаем репозиторий и загружаем начальное значение
    repository = CounterRepository()
    initial_value = repository.load_value()

    # 2. Создаем чистую модель с начальными данными
    model = CounterModel(initial_value=initial_value)

    # 3. Передаем в роутер модель и репозиторий для сохранения при выходе
    router = AppRouter(model=model, repository=repository)
    router.start()
    router.hide_splash_screen()

    # 4. Запускаем главный бесконечный цикл приложения
    app.MainLoop()

if __name__ == '__main__':
    main() 