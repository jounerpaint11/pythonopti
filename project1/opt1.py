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

# --- Очистка временных файлов ---
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

# --- Мониторинг ресурсов через команду Linux ---
def monitor_resources():
    log("=== Мониторинг ресурсов ===")
    log("CPU и память (через top):")
    os.system("top -b -n1 | head -n 10")
    log("Диск:")
    os.system("df -h /")

# --- Поиск больших файлов ---
def find_big_files(path="/home"):
    log(f"=== Поиск файлов >{BIG_FILE_SIZE_MB}MB ===")
    for root, dirs, files in os.walk(path):
        for name in files:
            try:
                full_path = os.path.join(root, name)
                size_mb = os.path.getsize(full_path) / (1024*1024)
                if size_mb > BIG_FILE_SIZE_MB:
                    log(f"{full_path} - {size_mb:.2f} MB")
            except:
                continue

# --- Очистка кеша Linux ---
def drop_caches():
    log("=== Очистка кеша Linux ===")
    if os.geteuid() != 0:
        log("Нужны root-права для очистки кеша")
        return
    os.system("sync && echo 3 | sudo tee /proc/sys/vm/drop_caches")
    log("Кеш очищен")

def main():
    log("=== Запуск оптимизатора ===")
    monitor_resources()
    clean_temp_dirs()
    find_big_files()
    drop_caches()
    log("=== Оптимизация завершена ===\n\n")

if __name__ == "__main__":
    main()
