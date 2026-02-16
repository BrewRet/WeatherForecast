import os
import sys

VENV_PATH = os.path.join(os.path.dirname(__file__), '.venv')

def running_in_venv():
    """Проверяет, запущен ли скрипт из данного виртуального окружения."""
    return sys.prefix == VENV_PATH

def restart_in_venv():
    """Перезапускает текущий скрипт с интерпретатором из .venv."""
    if sys.platform == 'win32':
        python_exe = os.path.join(VENV_PATH, 'Scripts', 'python.exe')
    else:
        python_exe = os.path.join(VENV_PATH, 'bin', 'python')

    if not os.path.exists(python_exe):
        print(f"Ошибка: интерпретатор в {python_exe} не найден.")
        sys.exit(1)

    os.execv(python_exe, [python_exe] + sys.argv)

if os.path.isdir(VENV_PATH) and not running_in_venv():
    restart_in_venv()


import uvicorn

from app.config import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)