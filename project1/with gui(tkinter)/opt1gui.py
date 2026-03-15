#!/usr/bin/env python3

import subprocess
import os
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

REPORT_FILE = os.path.expanduser("~/system_optimization_report.txt")
BIG_FILE_SIZE_MB = 100
TEMP_DIRS = ["/tmp", os.path.expanduser("~/.cache")]

def log(msg):
    clean_msg = str(msg).strip()
    text_area.insert(tk.END, f"{clean_msg}\n")
    text_area.see(tk.END)

    try:
        with open(REPORT_FILE, "a") as f:
            f.write(f"{datetime.now()} - {clean_msg}\n")
    except Exception as e:
        print(f"Ошибка записи в лог: {e}")

def clean_temp():
    log("=== Очистка временных файлов ===")
    for d in TEMP_DIRS:
        if os.path.exists(d):
            for root_dir, dirs, files in os.walk(d, topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root_dir, name))
                    except: pass
                for name in dirs:
                    try:
                        shutil.rmtree(os.path.join(root_dir, name))
                    except: pass
    log("Очистка завершена")

def monitor():
    log("=== Мониторинг системы ===")
    try:
        cpu = subprocess.check_output("top -b -n1 | head -n 5", shell=True, text=True)
        log("CPU / RAM:\n" + cpu)
        
        disk = subprocess.check_output("df -h /", shell=True, text=True)
        log("Диски:\n" + disk)
    except Exception as e:
        log(f"Ошибка мониторинга: {e}")

def find_big():
    log(f"=== Поиск файлов > {BIG_FILE_SIZE_MB}MB ===")
    home_path = os.path.expanduser("~")
    for root_dir, dirs, files in os.walk(home_path):
        for name in files:
            try:
                path = os.path.join(root_dir, name)
                if not os.path.islink(path):
                    size = os.path.getsize(path) / (1024 * 1024)
                    if size > BIG_FILE_SIZE_MB:
                        log(f"{path} - {size:.2f} MB")
            except: pass
    log("Поиск завершен")

def drop_cache():
    log("=== Очистка кеша Linux ===")
    cmd = "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches"
    try:
        subprocess.run(f"xterm -e 'echo Нужны права root; {cmd}'", shell=True)
        log("Команда отправлена (проверьте окно терминала)")
    except:
        log("Ошибка: установите xterm или запустите скрипт через sudo")

def show_report():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            content = f.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, content)
    else:
        messagebox.showinfo("Инфо", "Отчёт еще не создан")

root = tk.Tk()
root.title("Linux System Optimizer (Ubuntu)")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Мониторинг", width=25, command=monitor).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame, text="Очистить temp", width=25, command=clean_temp).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame, text="Найти большие файлы", width=25, command=find_big).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame, text="Очистить кеш (Sudo)", width=25, command=drop_cache).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame, text="Показать весь лог", width=25, command=show_report).grid(row=2, column=0, columnspan=2, pady=5)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root.mainloop()
