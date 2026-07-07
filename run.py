from app import MyApplication

def main():
    # 1. Инициализируем приложение wxPython c графическим пользовательским интерфейсом
    app = MyApplication()
    # 2. Запускаем главный бесконечный цикл приложения
    app.MainLoop()

if __name__ == '__main__':
    main() 