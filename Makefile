# Makefile для проекта wxPython MVP
# Для Windows используйте build.bat или запускайте через WSL
# Для Linux/Mac используйте make <target>

PYTHON_CMD=python3
VENV_DIR=.venv
REQUIREMENTS_LINUX=./requirements/linux/requirements.txt
BUILD_DIR=.build

.PHONY: venv run test clean help

help:
	@echo "Доступные цели:"
	@echo "  venv    - Создать виртуальное окружение и установить зависимости"
	@echo "  run     - Запустить приложение"
	@echo "  test    - Запустить тесты"
	@echo "  clean   - Очистить временные файлы и виртуальное окружение"
	@echo "  help    - Показать это сообщение"

venv:
	@echo "Создание виртуального окружения..."
	$(PYTHON_CMD) -m venv $(VENV_DIR)
	@echo "Активация виртуального окружения и установка зависимостей..."
	. $(VENV_DIR)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r $(REQUIREMENTS_LINUX)
	@echo "Виртуальное окружение готово"

run: venv
	@echo "Запуск приложения..."
	. $(VENV_DIR)/bin/activate && $(PYTHON_CMD) run.py

test:
	@echo "Запуск тестов..."
	$(PYTHON_CMD) -m unittest discover tests -v

clean:
	@echo "Очистка проекта..."
	rm -rf $(VENV_DIR) $(BUILD_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.log" -delete 2>/dev/null || true
	@echo "Очистка завершена"

