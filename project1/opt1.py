#!/usr/bin/env python3

import os
import shutil
import subprocess
from datetime import datetime

REPORT_FILE = os.path.expanduser("~/system_optimization_report.txt")
BIG_FILE_SIZE_MB = 100
TEMP_DIRS = ["/tmp", os.path.expanduser("~/.cache")]


def log(msg):
    formatted_msg = str(msg).strip()
    with open(REPORT_FILE, "a") as f:
        f.write(f"{datetime.now()} - {formatted_msg}\n")
    print(formatted_msg)


def clean_temp_dirs():
    log("=== Очистка временных файлов ===")

    for d in TEMP_DIRS:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception:
                        pass

                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, name))
                    except Exception:
                        pass

    log("Очистка завершена")


def monitor_resources():
    log("=== Мониторинг ресурсов ===")

    log("CPU и память:")
    try:
        top_output = subprocess.check_output("top -b -n1 | head -n 10", shell=True, text=True)
        log(top_output)
    except Exception as e:
        log(f"Ошибка получения данных CPU: {e}")

    log("Диск:")
    try:
        df_output = subprocess.check_output("df -h /", shell=True, text=True)
        log(df_output)
    except Exception as e:
        log(f"Ошибка получения данных диска: {e}")


def find_big_files(path="/home"):
    log(f"=== Поиск файлов > {BIG_FILE_SIZE_MB}MB ===")

    for root, dirs, files in os.walk(path):
        for name in files:
            try:
                full_path = os.path.join(root, name)
                if not os.path.islink(full_path):
                    size_mb = os.path.getsize(full_path) / (1024 * 1024)

                    if size_mb > BIG_FILE_SIZE_MB:
                        log(f"{full_path} - {size_mb:.2f} MB")

            except Exception:
                continue


def drop_caches():
    log("=== Очистка кеша Linux ===")


    try:
        subprocess.run("sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null", shell=True, check=True)
        log("Кеш очищен")
    except subprocess.CalledProcessError:
        log("Ошибка: не удалось очистить кеш (отменено пользователем или нет прав)")


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
