#!/usr/bin/env python3

import subprocess
import os
import shutil
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

REPORT_FILE = "/tmp/system_optimization_report.txt"
BIG_FILE_SIZE_MB = 100
TEMP_DIRS = ["/tmp", os.path.expanduser("~/.cache")]


def log(msg):
    text.insert(tk.END, msg + "\n")
    text.see(tk.END)

    with open(REPORT_FILE, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")


def clean_temp():
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


def monitor():

    log("=== Мониторинг системы ===")

    log("CPU / RAM:")
    result = subprocess.check_output(
        "top -b -n1 | head -n 5",
        shell=True,
        text=True
    )
    log(result)

    log("Диски:")
    result = subprocess.check_output(
        "df -h /",
        shell=True,
        text=True
    )
    log(result)


def find_big():
    log(f"=== Поиск файлов > {BIG_FILE_SIZE_MB}MB ===")

    for root_dir, dirs, files in os.walk("/home"):

        for name in files:
            try:
                path = os.path.join(root_dir, name)
                size = os.path.getsize(path) / (1024 * 1024)

                if size > BIG_FILE_SIZE_MB:
                    log(f"{path} - {size:.2f} MB")

            except:
                pass


def drop_cache():
    log("=== Очистка кеша Linux ===")

    if os.geteuid() != 0:
        log("Нужен sudo")
        return

    os.system("sync && echo 3 | sudo tee /proc/sys/vm/drop_caches")
    log("Кеш очищен")


def show_report():

    log("=== Отчёт ===")

    if os.path.exists(REPORT_FILE):

        with open(REPORT_FILE) as f:
            text.insert(tk.END, f.read())


root = tk.Tk()
root.title("Linux System Optimizer")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Мониторинг", width=20, command=monitor).grid(row=0, column=0)
tk.Button(frame, text="Очистить temp", width=20, command=clean_temp).grid(row=0, column=1)
tk.Button(frame, text="Найти большие файлы", width=20, command=find_big).grid(row=1, column=0)
tk.Button(frame, text="Очистить кеш", width=20, command=drop_cache).grid(row=1, column=1)
tk.Button(frame, text="Показать отчёт", width=20, command=show_report).grid(row=2, column=0)

text = scrolledtext.ScrolledText(root)
text.pack(fill="both", expand=True)

root.mainloop()

