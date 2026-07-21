@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:: ========================================
::    Конфигурационные переменные
:: ========================================
set "BUILD_DIR=.build"
set "VENV_DIR=.venv"
set "EXE_NAME=mvp-wxpython-app-windows-i386.exe"
set "ICON_FILE_PATH=app\assets\icons\app-icon.ico"
set "SPLASH_SCREEN_FILE_PATH=app\assets\images\logo.png"
set "FILE_VERSION=1.0.0.0"
set "PRODUCT_VERSION=1.0.0.0"
set "COMPANY_NAME=UIMDB"
set "PRODUCT_NAME=mvp-wxpython-example-app"
set "PYTHON_CMD=py -3.7"
:: Настройка путей к ресурсам проекта
set "ASSETS_SRC=app\assets"
set "ASSETS_DST=app\assets"   

:menu
cls
echo ========================================
echo    Скрипт сборки Python проекта
echo ========================================
echo.
echo Выберите действие:
echo   1 - Собрать исполняемый файл
echo   2 - Запустить исполняемый файл
echo   3 - Очистка проекта
echo   4 - Запустить тесты
echo   5 - Выход
echo.
set /p choice="Введите номер действия (1-5): "

if "%choice%"=="1" goto build
if "%choice%"=="2" goto run
if "%choice%"=="3" goto clean
if "%choice%"=="4" goto run_tests
if "%choice%"=="5" goto exit
echo Неверный выбор! Пожалуйста, введите 1, 2, 3, 4 или 5
pause
goto menu

:run_tests
call :run_tests_only
goto menu

:build
call :build_executable
goto menu

:run
if exist "%BUILD_DIR%\%EXE_NAME%" (
    echo Запуск исполняемого файла...
    "%BUILD_DIR%\%EXE_NAME%"
) else (
    echo Исполняемый файл не найден. Собираю проект...
    call :build_executable
    if exist "%BUILD_DIR%\%EXE_NAME%" (
        echo Запуск исполняемого файла...
        "%BUILD_DIR%\%EXE_NAME%"
    ) else (
        echo Ошибка: не удалось собрать или найти исполняемый файл
        pause
    )
)
goto menu

:clean
echo.
echo ========================================
echo    Очистка проекта
echo ========================================

echo Удаление директории сборки...
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo Директория %BUILD_DIR% удалена
)

echo Удаление директории виртуального окружения...
if exist "%VENV_DIR%" (
    rmdir /s /q "%VENV_DIR%"
    echo Директория %VENV_DIR% удалена
)

echo Удаление кэша Python...
for /d /r . %%i in (__pycache__) do (
    if exist "%%i" (
        rmdir /s /q "%%i"
        
    )
)

echo Удаление временных файлов...
if exist "*.log" del /q *.log 2>nul
if exist "*.spec" del /q *.spec 2>nul
if exist "*.coverage" del /q *.coverage 2>nul
if exist ".dist" rmdir /s /q ".dist" 2>nul
if exist ".build" rmdir /s /q ".build" 2>nul

echo Удаление кэша Nuitka...
if exist ".nuitka" rmdir /s /q ".nuitka" 2>nul

echo Очистка завершена!
pause
goto menu

:exit
echo Выход...
timeout /t 1 >nul
cls
exit /b 0

:check_py_launcher
py --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python Launcher не установлен
    echo Установите Python из официального сайта python.org
    pause
    exit /b 1
)
goto :eof 

:check_python
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Python не установлен или не добавлен в PATH
    echo Убедитесь, что Python установлен и доступен из командной строки
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import sys; exit(0) if sys.version_info[:2] == (3, 7) else exit(1)" >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Требуется Python 3.7
    echo.
    %PYTHON_CMD% --version
    echo.
    echo Установите Python 3.7 и повторите попытку
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import sys; exit(0) if sys.maxsize <= 2**32 else exit(1)" >nul 2>&1
if errorlevel 1 (
    echo Ошибка: Требуется 32-битная версия Python 3.7
    echo.
    %PYTHON_CMD% --version
    echo Обнаружена 64-битная версия
    echo.
    echo Установите 32-битную версию Python 3.7 и повторите попытку
    pause
    exit /b 1
)

echo ✓ Python 3.7 32-bit подтвержден
goto :eof

:build_executable
cls
echo.
echo ========================================
echo    Начало процесса сборки
echo ========================================

call :check_py_launcher
if errorlevel 1 (
    echo Проверка py launcher не пройдена. Сборка прервана.
    pause
    exit /b 1
)

call :check_python
if errorlevel 1 (
    echo Проверка Python не пройдена. Сборка прервана.
    pause
    exit /b 1
)

if not exist "run.py" (
    echo Ошибка: Файл run.py не найден!
    pause
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo Виртуальное окружение не найдено. Создаю...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        echo Ошибка создания виртуального окружения
        pause
        exit /b 1
    )
    echo Виртуальное окружение успешно создано
) else (
    echo Виртуальное окружение найдено
)

echo Активация виртуального окружения...
call "%VENV_DIR%\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo Ошибка активации виртуального окружения
    pause
    exit /b 1
)

echo Проверка активации виртуального окружения...
python -c "import sys; print('Python path:', sys.prefix)" | find "%VENV_DIR%" >nul
if errorlevel 1 (
    echo Ошибка: виртуальное окружение не активировано правильно
    pause
    exit /b 1
)

echo Обновление pip...
python -m pip install --upgrade pip
if !errorlevel! neq 0 (
    echo Предупреждение: не удалось обновить pip, продолжение с текущей версией
    echo Проверка версии pip...
    python -m pip --version
) else (
    echo Pip успешно обновлен
    python -m pip --version
)

if exist "./requirements/windows/x86/requirements.txt" (
    echo Установка зависимостей из requirements.txt...
    python -m pip install -r ./requirements/windows/x86/requirements.txt
    if !errorlevel! neq 0 (
        echo Ошибка установки зависимостей
        pause
        exit /b 1
    )
    echo Зависимости успешно установлены
) else (
    echo Файл ./requirements/windows/x86/requirements.txt не найден, пропускаю установку зависимостей
)

echo Запуск сборки с помощью Nuitka...

:: для Nuitka>=2.6.7 и wxPython==4.1.1
set "NUITKA_CMD=python -m nuitka"
set "NUITKA_CMD=!NUITKA_CMD! --mode=onefile"
set "NUITKA_CMD=!NUITKA_CMD! --windows-console-mode=disable"
set "NUITKA_CMD=!NUITKA_CMD! --assume-yes-for-downloads"
set "NUITKA_CMD=!NUITKA_CMD! --include-package=wx"
set "NUITKA_CMD=!NUITKA_CMD! --include-package-data=wx"
set "NUITKA_CMD=!NUITKA_CMD! --noinclude-unittest-mode=nofollow"
set "NUITKA_CMD=!NUITKA_CMD! --noinclude-setuptools-mode=nofollow"
set "NUITKA_CMD=!NUITKA_CMD! --include-data-dir=!ASSETS_SRC!=!ASSETS_DST!"
set "NUITKA_CMD=!NUITKA_CMD! --company-name=%COMPANY_NAME%"
set "NUITKA_CMD=!NUITKA_CMD! --product-name=%PRODUCT_VERSION%"
set "NUITKA_CMD=!NUITKA_CMD! --windows-file-version=%FILE_VERSION%"
set "NUITKA_CMD=!NUITKA_CMD! --windows-product-version=%PRODUCT_VERSION%"
set "NUITKA_CMD=!NUITKA_CMD! --report=.\%BUILD_DIR%\report.xml"
set "NUITKA_CMD=!NUITKA_CMD! --output-dir=.\%BUILD_DIR%"
set "NUITKA_CMD=!NUITKA_CMD! --output-filename=%EXE_NAME%"

if exist "%ICON_FILE_PATH%" (
    set "NUITKA_CMD=!NUITKA_CMD! --windows-icon-from-ico=%ICON_FILE_PATH%"
) else (
    echo Предупреждение: файл иконки не найден - %ICON_FILE_PATH%
)

if exist "%SPLASH_SCREEN_FILE_PATH%" (
    set "NUITKA_CMD=!NUITKA_CMD! --onefile-windows-splash-screen-image=%SPLASH_SCREEN_FILE_PATH%"
) else (
    echo Предупреждение: файл splash screen не найден - %SPLASH_SCREEN_FILE_PATH%
)


echo Выполняется: !NUITKA_CMD! .\run.py
call !NUITKA_CMD! .\run.py

if !errorlevel! neq 0 (
    echo Сборка завершилась с ошибкой!
    cd /d "%ORIGINAL_DIR%"
    pause
    exit /b 1
)

echo Сборка успешно завершена!

echo Деактивация виртуального окружения...
call "%VENV_DIR%\Scripts\deactivate.bat"
if !errorlevel! neq 0 (
    echo Ошибка активации виртуального окружения
    pause
    exit /b 1
)

echo ========================================
echo    Процесс сборки завершен!
echo ========================================

if exist "%BUILD_DIR%\%EXE_NAME%" (
    echo Собранный файл: %BUILD_DIR%\%EXE_NAME%
    for %%F in ("%BUILD_DIR%\%EXE_NAME%") do (
        echo Размер файла: %%~zF байт
    )
) else (
    echo ВНИМАНИЕ: исполняемый файл не найден в папке %BUILD_DIR%!
)

pause
exit /b 0

:run_tests_only
cls
echo.
echo ========================================
echo    Запуск тестов
echo ========================================

call :check_py_launcher
if errorlevel 1 (
    echo Проверка py launcher не пройдена.
    pause
    exit /b 1
)

call :check_python
if errorlevel 1 (
    echo Проверка Python не пройдена.
    pause
    exit /b 1
)

if not exist "run.py" (
    echo Ошибка: Файл run.py не найден!
    pause
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo Виртуальное окружение не найдено. Создаю...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
    if !errorlevel! neq 0 (
        echo Ошибка создания виртуального окружения
        pause
        exit /b 1
    )
    echo Виртуальное окружение успешно создано
) else (
    echo Виртуальное окружение найдено
)

echo Активация виртуального окружения...
call "%VENV_DIR%\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo Ошибка активации виртуального окружения
    pause
    exit /b 1
)

echo Проверка активации виртуального окружения...
python -c "import sys; print('Python path:', sys.prefix)" | find "%VENV_DIR%" >nul
if errorlevel 1 (
    echo Ошибка: виртуальное окружение не активировано правильно
    pause
    exit /b 1
)

echo Обновление pip...
python -m pip install --upgrade pip
if !errorlevel! neq 0 (
    echo Предупреждение: не удалось обновить pip, продолжение с текущей версией
) else (
    echo Pip успешно обновлен
)

if exist "./requirements/windows/x86/requirements.txt" (
    echo Установка зависимостей из requirements.txt...
    python -m pip install -r ./requirements/windows/x86/requirements.txt
    if !errorlevel! neq 0 (
        echo Ошибка установки зависимостей
        pause
        exit /b 1
    )
    echo Зависимости успешно установлены
) else (
    echo Файл ./requirements/windows/x86/requirements.txt не найден, пропускаю установку зависимостей
)

echo.
echo ========================================
echo    Запуск тестов
echo ========================================
python -m unittest discover tests -v
if !errorlevel! neq 0 (
    echo.
    echo Ошибка: тесты не прошли!
    pause
    exit /b 1
)
echo.
echo ✓ Все тесты успешно пройдены!
echo.

echo Деактивация виртуального окружения...
call "%VENV_DIR%\Scripts\deactivate.bat"
if !errorlevel! neq 0 (
    echo Ошибка деактивации виртуального окружения
    pause
    exit /b 1
)

pause
exit /b 0