@echo off
REM Имя виртуального окружения
set VENV_NAME=.venv

REM Команды для создания и активации виртуального окружения
set VENV_ACTIVATE=%VENV_NAME%\Scripts\activate

REM Зависимости проекта (укажите все необходимые пакеты)
set REQUIREMENTS=requirements.txt

REM Создание виртуального окружения
if not exist %VENV_NAME% (
    python -m venv %VENV_NAME%
)

REM Активация виртуального окружения
call %VENV_ACTIVATE%

REM Установка зависимостей
pip install --upgrade pip
pip install -r %REQUIREMENTS%

REM Запуск приложения
python main.py