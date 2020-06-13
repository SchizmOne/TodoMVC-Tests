from time import sleep
import logging
import os
import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class TestChrome:

    browser = None
    if os.name == "nt":
        PATH_TO_WEBDRIVER = os.path.join(os.getcwd(), "webdrivers", "chromedriver.exe")
    else:
        PATH_TO_WEBDRIVER = os.path.join(os.getcwd(), "webdrivers", "chromedriver")

    def setup_class(self):

        # Запускаем Chromedriver.
        self.browser = Chrome(executable_path=self.PATH_TO_WEBDRIVER)

        # Выставляем время, которое будет дано браузеру, чтобы найти элементы
        # или завершить какую-либо операцию.
        self.browser.implicitly_wait(3)

    def setup_method(self):

        # Ссылка на TodoMVC
        url = "http://todomvc.com/examples/react/"
        # Открываем TodoMVC в браузере.
        self.browser.get(url)

    def teardown_method(self):

        self.browser.execute_script("window.localStorage.clear();")
        self.browser.refresh()

    def teardown_class(self):

        self.browser.close()
        self.browser.quit()

    def test_opening_and_finding_input(self):
        """TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC

        Данный тест-кейс предназначен для проверки того, что приложение в
        принципе открывается в браузере при переходе по ссылке, а также
        то, что оно отрисует необходимый элемент для ввода задачи.
        """

        logging.info("TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC")

        # Ожидаемый заголовок страницы.
        title = "React • TodoMVC"
        # Ожидаемый текст по умолчанию в поле для ввода.
        placeholder_text = "What needs to be done?"

        sleep(1)

        # Находим заголовок страницы и сравниваем с ожидаемым.
        page_title = self.browser.title
        assert page_title == title

        # Проверяем, что на странице есть элемент для ввода новой задачи.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        assert new_todo is not None

        # Проверяем, что текст по умолчанию в поле для ввода соответствует ожидаемому.
        placeholder = new_todo.get_attribute("placeholder")
        assert placeholder == placeholder_text

    def test_adding_task(self):
        """TC ID: TodoMVC-1 - Добавить новую задачу

        Данный тест-кейс предназначен для проверки того, что
        пользователь может добавить в поле для ввода название
        новой задачи, после чего она будет добавлена в список
        с тем же названием, которое ввел пользователь.
        """

        logging.info("TC ID: TodoMVC-1 - Добавить новую задачу")

        # Текст с названием задачи.
        new_task_name = "TC ID: TodoMVC-1 - Добавить новую задачу"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(new_task_name + Keys.ENTER)

        sleep(1)

        # Проверяем, что появился элемент списка.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        assert todo_list is not None

        # Проверяем, что в нем появилась новая задача.
        task = todo_list.find_element_by_tag_name("li")
        assert task is not None

        # Проверяем, что название задачи совпадает с введенным.
        task_name = task.find_element_by_tag_name("label").text
        assert task_name == new_task_name

        # Проверяем, что в нижней части формы появилась
        # панель для фильтрации и управления списком.
        footer = self.browser.find_element_by_class_name("footer")
        assert footer is not None

    def test_adding_task_to_non_empty_list(self):
        """TC ID: TodoMVC-2 - Добавить новую задачу в непустой список

        Данный тест-кейс предназначен для проверки того, что
        пользователь может добавить новую задачу в список, где
        задача уже была добавлена, и что в списке уже будет обе
        задачи.
        """

        logging.info("TC ID: TodoMVC-2 - Добавить новую задачу в непустой список")

        # Список названий задач.
        task_names = ["Задача 1", "Задача 2"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for new_task in task_names:
            new_todo.send_keys(new_task, Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")

        sleep(1)

        # Проверяем, что поиск элементов-зачач теперь вернет список,
        # соответствующий по длине тому, что был изначально.
        tasks = todo_list.find_elements_by_tag_name("li")
        assert len(tasks) == len(task_names)

        # Проверяем, что названия задач в списке соответствуют тем,
        # которые были в списке изначально.
        for task in tasks:
            task_name = task.find_element_by_tag_name("label").text
            is_task_name_correct = task_name in task_names
            assert is_task_name_correct is True

    def test_delete_task(self):
        """TC ID: TodoMVC-3 - Удалить задачу

        Данный тест-кейс предназначен для проверки того, что
        пользователь может добавить задачу, а после этого
        удалить её из списка.
        """

        logging.info("TC ID: TodoMVC-3 - Удалить задачу")

        # Текст с названием задачи.
        task_name = "Задача под удаление"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(task_name + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него задачу.
        task = todo_list.find_element_by_tag_name("li")

        sleep(1)

        # Нажимаем на кнопку удаления задачи.
        #
        # (Примечание: Видимо, click() обычный не работает, когда
        # кнопка отображается только при наведении курсора. StackOverflow
        # подсказывает, что это проблема Selenium и советует использовать
        # готовый JS-код для клика на кнопки в таких ситуациях.
        destroy_button = task.find_element_by_class_name("destroy")
        self.browser.execute_script("arguments[0].click();", destroy_button)

        # Проверяем, что списка больше не существует.
        # todo_list = self.browser.find_elements_by_class_name("todo-list")
        # assert todo_list == []
        with pytest.raises(NoSuchElementException):
            self.browser.find_element_by_xpath("todo-list")
