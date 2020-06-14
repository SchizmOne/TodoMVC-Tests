# -*- coding: utf-8 -*-

"""Автор: schizm.one@gmail.com
Данный сценарий предназначен для подготовки окружения
к запуску тестов. Это включает в себя создание виртуального
окружения, скачивание модулей для него, чтобы в дальнейшем
тесты могли быть запущены.
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
    CMD_FOR_DOWNLOADING_MODULES_TO_VENV = r"venv\Scripts\pip install -r {}" \
        .format(REQUIREMENTS_FILE_NAME)
# Команды для Linux.
else:
    CMD_FOR_CREATING_VENV = "python3 -m venv venv"
    CMD_FOR_DOWNLOADING_MODULES_TO_VENV = "venv/bin/pip3 install -r {}" \
        .format(REQUIREMENTS_FILE_NAME)

# Создаем директорию для веб-драйверов.
if not os.path.isdir(WEBDRIVER_DIRECTORY):

    print("Creating directory for web-drivers...")
    try:
        os.mkdir(WEBDRIVER_DIRECTORY)
        print("Successfully created the directory '{}'".format(WEBDRIVER_DIRECTORY))
        IS_WEBDRIVER_DIRECTORY_EXISTS = True
    except OSError:
        print("Creation of the directory '{}' failed".format(WEBDRIVER_DIRECTORY))
        IS_WEBDRIVER_DIRECTORY_EXISTS = False
else:
    IS_WEBDRIVER_DIRECTORY_EXISTS = True

# Создаем виртуальное окружение и получаем код завершения.
if not os.path.isdir(os.path.join(CURRENT_DIRECTORY, "venv")):
    print("Creating virtual environment...")
    return_code = os.system(CMD_FOR_CREATING_VENV)

    # Если код завершения - 0, то значит, что окружение было
    # успешно создано.
    if return_code == 0:
        print("Successfully created the virtual environment in 'venv'.")
        IS_VIRTUALENV_EXISTS = True
    else:
        print("Error in creating virtual environment!")
        IS_VIRTUALENV_EXISTS = False
else:
    IS_VIRTUALENV_EXISTS = True

# Загружаем модули для виртуального окружения
print("Downloading modules for virtual environment...")
return_code = os.system(CMD_FOR_DOWNLOADING_MODULES_TO_VENV)

# Если код завершения - 0, то значит, что все модули были загружены.
if return_code == 0:
    print("Successfully downloaded all modules for virtual environment.")
    IS_MODULES_DOWNLOADED = True
else:
    print("Error in downloading modules for virtual environment!")
    IS_MODULES_DOWNLOADED = False

# Выводим итоги.
print("\n\n====================== SUMMARY ======================\n" +
      "Webdriver directory created: {}\n".format(IS_WEBDRIVER_DIRECTORY_EXISTS) +
      "Virtual Environment created: {}\n".format(IS_VIRTUALENV_EXISTS) +
      "Modules downloaded to virtual environment: {}\n".format(IS_MODULES_DOWNLOADED))

if IS_WEBDRIVER_DIRECTORY_EXISTS and \
        IS_VIRTUALENV_EXISTS and IS_MODULES_DOWNLOADED:
    print("Successfully completed setting up testing environment.")
else:
    print("If something from the summary isn't 'True', than try to setting up\n" +
          "by following instructions in the file called 'README.MD'")
