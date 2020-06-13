 # -*- coding: utf-8 -*-

"""Автор: schizm.one@gmail.com
Данный сценарий предназначен для подготовки окружения
к запуску тестов. Это включает в себя создание виртуального
окружения, скачивание модулей для него, а также скачивание
драйверов для веб-браузеров и редактирование переменной
PATH, чтобы в дальнейшем тесты могли вызывать драйвера
для браузеров.
"""


import os


# Для начала, определим все постоянные данные,
# вроде типа ОС и названий файлов.
OS = os.name
REQUIREMENTS_FILE_NAME = "requirements.txt"
CURRENT_DIRECTORY = os.getcwd()
WEBDRIVER_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "webdrivers")

# Команды для Windows.
if OS == "nt":
    CMD_FOR_CREATING_VENV = "python -m venv venv"
    CMD_FOR_DOWNLOADING_MODULES_TO_VENV = r"venv\Scripts\pip install -r {}"\
                                        .format(REQUIREMENTS_FILE_NAME)
    CMD_FOR_SET_PATH = 'setx path "%path%{}{}"'.format(os.pathsep, WEBDRIVER_DIRECTORY)
# Команды для Linux.
else:
    CMD_FOR_CREATING_VENV = "python3 -m venv venv"
    CMD_FOR_DOWNLOADING_MODULES_TO_VENV = "venv/bin/pip3 install -r {}"\
                                        .format(REQUIREMENTS_FILE_NAME)
    CMD_FOR_SET_PATH = 'setx path "%path%{}{}"'.format(os.pathsep, WEBDRIVER_DIRECTORY)

# Создаем виртуальное окружение и получаем код завершения.
print("Creating virtual environment...")
return_code = os.system(CMD_FOR_CREATING_VENV)

# Если код завершения - 0, то значит, что окружение было
# успешно создано.
if return_code == 0:
    print("Virtual environment successfully created.")
else:
    print("Error in creating virtual environment!")

# Загружаем модули для виртуального окружения
print("Downloading modules for virtual environment...")
return_code = os.system(CMD_FOR_DOWNLOADING_MODULES_TO_VENV)

# Если код завершения - 0, то значит, что все модули были загружены.
if return_code == 0:
    print("All modules for virtual environment have been sucessfully downloaded.")
else:
    print("Error in downloading modules for virtual environment!")

# Создаем новую переменную для PATH, включающую
# директорию с драйвером для браузера.
print("Editing PATH...")
return_code = os.system(CMD_FOR_SET_PATH)

# Если код завершения - 0, то значит, что редактирование PATH прошло успешно.
if return_code == 0:
    print("Successfully edited PATH. Now, restart your terminal.")
else:
    print("Error in editing PATH!")
