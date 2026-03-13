#!/usr/bin/env python3

import os
import shutil
from datetime import datetime

REPORT_FILE = "/tmp/system_optimization_report.txt"
BIG_FILE_SIZE_MB = 100
TEMP_DIRS = ["/tmp", os.path.expanduser("~/.cache")]


def log(msg):
    with open(REPORT_FILE, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)


def clean_temp_dirs():
    log("=== Очистка временных файлов ===")

    for d in TEMP_DIRS:
        if os.path.exists(d):
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

    log("CPU и память:")
    os.system("top -b -n1 | head -n 10")

    log("Диск:")
    os.system("df -h /")


def find_big_files(path="/home"):
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


def drop_caches():
    log("=== Очистка кеша Linux ===")

    if os.geteuid() != 0:
        log("Нужны root-права для очистки кеша")
        return

    os.system("sync && echo 3 | sudo tee /proc/sys/vm/drop_caches")
    log("Кеш очищен")


def show_report():
    print("\n=== ОТЧЁТ ===")

    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            print(f.read())
    else:
        print("Отчёт пуст")


def full_optimization():
    log("=== Полная оптимизация ===")

    monitor_resources()
    clean_temp_dirs()
    find_big_files()
    drop_caches()

    log("=== Оптимизация завершена ===\n")


def menu():

    while True:

        print("\n===== Linux System Optimizer =====")
        print("1. Мониторинг системы")
        print("2. Очистить временные файлы")
        print("3. Найти большие файлы")
        print("4. Очистить кеш Linux")
        print("5. Полная оптимизация")
        print("6. Показать отчёт")
        print("0. Выход")

        choice = input("Выберите вариант: ")

        if choice == "1":
            monitor_resources()

        elif choice == "2":
            clean_temp_dirs()

        elif choice == "3":
            path = input("Путь для сканирования (Enter = /home): ")
            if path.strip() == "":
                path = "/home"
            find_big_files(path)

        elif choice == "4":
            drop_caches()

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
