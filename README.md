# pythonopti

1️⃣ Скачать проект

Если установлен git:

git clone https://github.com/jounerpaint11/pythonopti
cd pythonopti


Если git нет — скачай ZIP на странице репозитория и распакуй.

2️⃣ Проверить установлен ли Python

Проект работает на Python.

Проверка:

python3 --version


Если версия появилась — Python уже установлен.

3️⃣ Установка Python (если его нет)
Debian / Ubuntu / Linux Mint
sudo apt update
sudo apt install python3

Arch / Manjaro
sudo pacman -S python

Fedora
sudo dnf install python3

openSUSE
sudo zypper install python3

Alpine Linux
sudo apk add python3

4️⃣ Сделать файл исполняемым

Если в начале файла есть строка:

#!/usr/bin/env python3


тогда можно запускать его как программу.

Дать права:

chmod +x opt1.py

5️⃣ Запуск скрипта

Способ 1 (обычный):

python3 opt1.py


Способ 2 (как программа):

./opt1.py

6️⃣ Если нужен root

Некоторые функции оптимизации требуют прав администратора.

Запуск:

sudo python3 opt1.py


или

sudo ./opt1.py
