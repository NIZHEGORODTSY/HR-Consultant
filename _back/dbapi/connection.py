import subprocess
import sys


def ssh_connect_via_serveo(alias, username, serveo_host="serveo.net"):
    """
    Подключается по SSH через Serveo.net
    
    Args:
        alias: ваш алиас на Serveo
        username: имя пользователя на целевой машине
        serveo_host: хост Serveo (по умолчанию serveo.net)
    """
    try:
        # Формируем команду
        cmd = [
            "ssh",
            "-J", serveo_host,
            f"{username}@{alias}"
        ]

        print(f"Выполняется команда: {' '.join(cmd)}")
        print("Для выхода используйте Ctrl+C или введите 'exit'")

        # Запускаем процесс
        process = subprocess.Popen(cmd)
        process.wait()

    except KeyboardInterrupt:
        print("\nПодключение прервано пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Пример использования
    alias = 'myalias'
    username = 'postgres'

    ssh_connect_via_serveo(alias, username)
