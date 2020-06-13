import pytest
import logging
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep

@pytest.fixture
def browser():

    # Запускаем Chromedriver
    driver = Chrome()

    # Ждем, пока все загрузится, прежде чем продолжать.
    driver.implicitly_wait(10)

    # Возвращаем драйвер браузера в вызывающую его функцию с тестом.
    yield driver

    # Когда заканчиваем работу, выходим из браузера.
    driver.quit()


def test_opening_and_finding_input(browser):
    """TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC

    Данный тест-кейс предназначен для проверки того, что приложение в
    принципе открывается в браузере при переходе по ссылке, а также
    то, что оно отрисует необходимый элемент для ввода задачи.
    """

    logging.info("TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC")

    # Ссылка на TodoMVC
    URL = "http://todomvc.com/examples/react/"
    # Ожидаемый заголовок страницы.
    TITLE = "React • TodoMVC"
    # Ожидаемый текст по умолчанию в поле для ввода.
    PLACEHOLDER_TEXT = "What needs to be done?"

    # Открываем TodoMVC в браузере.
    browser.get(URL)

    # Находим заголовок страницы и сравниваем с ожидаемым.
    page_title = browser.title
    assert page_title == TITLE

    # Проверяем, что на странице есть элемент для ввода новой задачи.
    new_todo = browser.find_element_by_class_name("new-todo")
    assert new_todo is not None

    # Проверяем, что текст по умолчанию в поле для ввода соответствует ожидаемому.
    placeholder = new_todo.get_attribute("placeholder")
    assert placeholder == PLACEHOLDER_TEXT


def test_adding_task(browser):
    """TC ID: TodoMVC-1 - Добавить новую задачу

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить в поле для ввода название
    новой задачи, после чего она будет добавлена в список
    с тем же названием, которое ввел пользователь.
    """

    # Ссылка на TodoMVC
    URL = "http://todomvc.com/examples/react/"
    # Текст с названием задачи.
    NEW_TASK_NAME = "TC ID: TodoMVC-1 - Добавить новую задачу"

    # Открываем TodoMVC в браузере.
    browser.get(URL)

    # Находим элемент для ввода новой задачи и записываем название.
    new_todo = browser.find_element_by_class_name("new-todo")
    new_todo.send_keys(NEW_TASK_NAME + Keys.ENTER)

    # Проверяем, что появился элемент списка.
    todo_list = browser.find_element_by_class_name("todo-list")
    assert todo_list is not None

    # Проверяем, что в нем появилась новая задача.
    task = todo_list.find_element_by_tag_name("li")
    assert task is not None

    # Проверяем, что название задачи совпадает с введенным.
    task_name = task.find_element_by_tag_name("label").text
    assert task_name == NEW_TASK_NAME

    # Проверяем, что в нижней части формы появилась
    # панель для фильтрации и управления списком.
    footer = browser.find_element_by_class_name("footer")
    assert footer is not None


def test_adding_task_to_non_empty_list(browser):
    """TC ID: TodoMVC-2 - Добавить новую задачу в непустой список

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить новую задачу в список, где
    задача уже была добавлена, и что в списке уже будет обе
    задачи.
    """

    # Ссылка на TodoMVC
    URL = "http://todomvc.com/examples/react/"
    # Список названий задач.
    TASK_NAMES = ["Задача 1", "Задача 2"]

    # Открываем TodoMVC в браузере.
    browser.get(URL)

    # Находим элемент для ввода новой задачи и записываем название.
    new_todo = browser.find_element_by_class_name("new-todo")
    for new_task in TASK_NAMES:
        new_todo.send_keys(new_task, Keys.ENTER)

    sleep(1)

    # Находим список.
    todo_list = browser.find_element_by_class_name("todo-list")

    # Проверяем, что поиск элементов-зачач теперь вернет список,
    # соответствующий по длине тому, что был изначально.
    tasks = todo_list.find_elements_by_tag_name("li")
    assert len(tasks) == len(TASK_NAMES)

    # Проверяем, что названия задач в списке соответствуют тем,
    # которые были в списке изначально.
    for task in tasks:
        task_name = task.find_element_by_tag_name("label").text
        is_task_name_correct = task_name in TASK_NAMES
        assert is_task_name_correct is True


def test_delete_task(browser):
    """TC ID: TodoMVC-3 - Удалить задачу

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить задачу, а после этого
    удалить её из списка.
    """

    # Ссылка на TodoMVC
    URL = "http://todomvc.com/examples/react/"
    # Текст с названием задачи.
    TASK_NAME = "Задача под удаление"

    # Открываем TodoMVC в браузере.
    browser.get(URL)

    sleep(1)

    # Находим элемент для ввода новой задачи и записываем название.
    new_todo = browser.find_element_by_class_name("new-todo")
    new_todo.send_keys(TASK_NAME + Keys.ENTER)

    # Находим список.
    todo_list = browser.find_element_by_class_name("todo-list")
    # Вытягиваем из него задачу.
    task = todo_list.find_element_by_tag_name("li")

    # Нажимаем на кнопку удаления задачи.
    #
    # (Примечание: Видимо, click() обычный не работает, когда
    # кнопка отображается только при наведении курсора. StackOverflow
    # подсказывает, что это проблема Selenium и советует использовать
    # готовый JS-код для клика на кнопки в таких ситуациях.
    destroy_button = task.find_element_by_class_name("destroy")
    browser.execute_script("arguments[0].click();", destroy_button)

    # Проверяем, что списка больше не существует.
    try:
        browser.find_element_by_class_name("todo-list")
        assert False
    except NoSuchElementException:
        assert True
