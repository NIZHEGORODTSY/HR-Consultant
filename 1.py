import subprocess
import time

# Список программ для запуска
programs = [
    "python _front/app.py",
    "python _back/app.py"
]

processes = []

# Запуск всех программ
for cmd in programs:
    processes.append(subprocess.Popen(cmd, shell=True))

# Ожидание завершения всех процессов