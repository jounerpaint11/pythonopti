#!/usr/bin/env python3
#THIS VERSION WILL NOT BE UPDATED FOR WINDOWS. THIS IS THE FIRST AND LAST VERSION.
import os
import shutil
from datetime import datetime

REPORT_FILE = os.path.join(os.environ["TEMP"], "system_optimization_report.txt")
BIG_FILE_SIZE_MB = 100
TEMP_DIRS = [
    os.environ.get("TEMP"),
    os.environ.get("TMP")
]


def log(msg):
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)


def clean_temp_dirs():
    log("=== Очистка временных файлов Windows ===")

    for d in TEMP_DIRS:
        if d and os.path.exists(d):

            for root, dirs, files in os.walk(d):

                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except:
                        pass

                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, name))
                    except:
                        pass

    log("Очистка завершена")


def monitor_resources():
    log("=== Мониторинг ресурсов ===")

    log("Процессы:")
    os.system("tasklist | more")

    log("Диски:")
    os.system("wmic logicaldisk get size,freespace,caption")


def find_big_files(path="C:\\Users"):
    log(f"=== Поиск файлов > {BIG_FILE_SIZE_MB}MB ===")

    for root, dirs, files in os.walk(path):
        for name in files:

            try:
                full_path = os.path.join(root, name)
                size_mb = os.path.getsize(full_path) / (1024 * 1024)

                if size_mb > BIG_FILE_SIZE_MB:
                    log(f"{full_path} - {size_mb:.2f} MB")

            except:
                continue


def clean_windows_cache():
    log("=== Очистка кеша Windows ===")

    os.system("del /q/f/s %TEMP%\\*")
    os.system("del /q/f/s C:\\Windows\\Temp\\*")

    log("Кеш очищен")


def show_report():
    print("\n=== ОТЧЁТ ===")

    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("Отчёт пуст")


def full_optimization():
    log("=== Полная оптимизация ===")

    monitor_resources()
    clean_temp_dirs()
    find_big_files()
    clean_windows_cache()

    log("=== Оптимизация завершена ===\n")


def menu():

    while True:

        print("\n===== Windows System Optimizer =====")
        print("1. Мониторинг системы")
        print("2. Очистить временные файлы")
        print("3. Найти большие файлы")
        print("4. Очистить кеш Windows")
        print("5. Полная оптимизация")
        print("6. Показать отчёт")
        print("0. Выход")

        choice = input("Выберите вариант: ")

        if choice == "1":
            monitor_resources()

        elif choice == "2":
            clean_temp_dirs()

        elif choice == "3":
            path = input("Путь для сканирования (Enter = C:\\Users): ")
            if path.strip() == "":
                path = "C:\\Users"
            find_big_files(path)

        elif choice == "4":
            clean_windows_cache()

        elif choice == "5":
            full_optimization()

        elif choice == "6":
            show_report()

        elif choice == "0":
            print("Выход...")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    menu()

