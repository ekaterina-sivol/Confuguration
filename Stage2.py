# Импорт модулей для работы с ОС, аргументами командной строки и конфигурационными файлами
import os
import sys
import argparse
import configparser

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None


class EmulatorConfig:
    def __init__(self):
        # Инициализация конфигурации значениями по умолчанию
        self.vfs_path = os.path.join(os.getcwd(), "vfs")  # Путь к виртуальной файловой системе
        self.prompt = "> "  # Пользовательское приглашение по умолчанию
        self.startup_script = None  # Путь к стартовому скрипту
        self.config_file = None  # Путь к конфигурационному файлу

    def debug_print(self):
        print("\n" + "=" * 50)
        print("ОТЛАДОЧНЫЙ ВЫВОД КОНФИГУРАЦИИ ЭМУЛЯТОРА")
        print("=" * 50)
        print(f"Путь к VFS: {self.vfs_path}")
        print(f"Пользовательское приглашение: {self.prompt}")
        print(f"Стартовый скрипт: {self.startup_script or '(не задан)'}")
        print(f"Конфигурационный файл: {self.config_file or '(не задан)'}")
        print("=" * 50)

def parse_arguments():
    #Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Эмулятор командной строки UNIX')

    # Добавление параметров командной строки
    parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
    parser.add_argument('--prompt', help='Пользовательское приглашение к вводу')
    parser.add_argument('--startup-script', help='Путь к стартовому скрипту')
    parser.add_argument('--config-file', help='Путь к конфигурационному файлу')

    # Парсинг аргументов
    return parser.parse_args()


def load_config_file(config_path):
    # Загрузка конфигурации из INI файла
    config = configparser.ConfigParser()

    # Проверка существования файла
    if not os.path.exists(config_path):
        print(f"Предупреждение: конфигурационный файл '{config_path}' не найден")
        return None

    try:
        # Чтение конфигурационного файла
        config.read(config_path, encoding='utf-8')
        return config
    except Exception as e:
        print(f"Ошибка при чтении конфигурационного файла: {e}")
        return None


def merge_configurations(cmd_args):
    # Объединение конфигураций из командной строки и файла
    emulator_config = EmulatorConfig()

    # Шаг 1: Загрузка значений из командной строки
    if cmd_args.vfs_path:
        emulator_config.vfs_path = cmd_args.vfs_path
    if cmd_args.prompt:
        emulator_config.prompt = cmd_args.prompt
    if cmd_args.startup_script:
        emulator_config.startup_script = cmd_args.startup_script
    if cmd_args.config_file:
        emulator_config.config_file = cmd_args.config_file

    # Шаг 2: Загрузка значений из конфигурационного файла (имеет приоритет)
    if emulator_config.config_file:
        file_config = load_config_file(emulator_config.config_file)

        if file_config and 'emulator' in file_config:
            # Чтение значений из секции [emulator] конфигурационного файла
            emulator_section = file_config['emulator']

            if 'vfs_path' in emulator_section:
                emulator_config.vfs_path = emulator_section['vfs_path']  # Приоритет файла
            if 'prompt' in emulator_section:
                emulator_config.prompt = emulator_section['prompt']  # Приоритет файла
            if 'startup_script' in emulator_section:
                emulator_config.startup_script = emulator_section['startup_script']  # Приоритет файла

    return emulator_config


def execute_startup_script(script_path):
    #Выполнение стартового скрипта
    print(f"\nВыполнение стартового скрипта: {script_path}")
    print("-" * 40)

    # Проверка существования скрипта
    if not os.path.exists(script_path):
        print(f"ОШИБКА: Скрипт '{script_path}' не найден!")
        return False

    try:
        # Чтение скрипта построчно
        with open(script_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Выполнение команд из скрипта
        for line_num, line in enumerate(lines, 1):
            command = line.strip()

            # Пропускаем пустые строки и комментарии
            if not command or command.startswith('#'):
                continue

            # Имитация диалога: отображение ввода
            print(f"[ВВОД] {command}")

            # Простая имитация вывода (в реальном эмуляторе здесь будет обработка команд)
            print(f"[ВЫВОД] Выполнена команда: {command}")

            # Проверка на команду выхода
            if command.lower() == 'exit':
                print("[ВЫВОД] Завершение работы по команде exit")
                return True

        print("-" * 40)
        print("Скрипт выполнен успешно")
        return True

    except Exception as e:
        print(f"ОШИБКА при выполнении скрипта: {e}")
        return False


def main():
    # Парсинг аргументов командной строки
    cmd_args = parse_arguments()

    # Объединение конфигураций из командной строки и файла
    emulator_config = merge_configurations(cmd_args)

    # Отладочный вывод конфигурации
    emulator_config.debug_print()

    # Выполнение стартового скрипта если задан
    if emulator_config.startup_script:
        if not execute_startup_script(emulator_config.startup_script):
            print("Завершение работы из-за ошибки в скрипте")
            return

    print("\nЭмулятор готов к работе. Конфигурация загружена успешно.")


# Стандартная проверка для запуска программы напрямую
if __name__ == "__main__":
    main()