import pytest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


def adding_task(task_names, driver):
    """Данная функция предназначена для добавления задачи
    в список задач.

    :param task_names: Имена задач. Может быть одной строкой или списком строк.
    :param driver: Объект браузера.
    """

    # Находим элемент для ввода новой задачи.
    new_todo = driver.find_element_by_class_name("new-todo")
    # Записываем имена всех задач, если их несколько.
    if isinstance(task_names, list):
        for task_name in task_names:
            new_todo.send_keys(task_name + Keys.ENTER)
    else:
        # Записываем имя задачи, если она одна.
        new_todo.send_keys(task_names + Keys.ENTER)


def delete_task(task, driver):
    """Данная функция предназначена для удаления задачи
    из списка задач.

    :param task: Объект задачи под удаление.
    :param driver: Объект браузера.
    """

    # Нажимаем на кнопку удаления задачи.
    #
    # (Примечание: Видимо, click() обычный не работает, когда
    # кнопка отображается только при наведении курсора. StackOverflow
    # подсказывает, что это проблема Selenium и советует использовать
    # готовый JS-код для клика на кнопки в таких ситуациях.
    destroy_button = task.find_element_by_class_name("destroy")
    driver.execute_script("arguments[0].click();", destroy_button)


def edit_task_name(task, new_task_name, driver):
    """Данная функция предназначена для изменения имени
    задачи в списке.

    :param task: Объект задачи под удаление.
    :param new_task_name: Новое имя задачи.
    :param driver: Объект браузера.
    """

    # Получаем предыдущее имя задачи.
    old_task_name = task.find_element_by_tag_name("label").text

    # Дважды кликаем на название задачи, чтобы она стала редактируемой.
    view = task.find_element_by_class_name("view")
    action_chains = ActionChains(driver)
    action_chains.double_click(view).perform()

    # Повторно вытягиваем задачу в режиме редактирования.
    edit_input = task.find_element_by_class_name("edit")
    # По очереди стираем все название до этого.
    for _ in old_task_name:
        edit_input.send_keys(Keys.BACK_SPACE)
    # Вводим новое название.
    edit_input.send_keys(new_task_name, Keys.ENTER)


def mark_task_as_completed(task, driver):
    """Данная функция предназначена для отметки
    задачи как 'выполненной'.

    :param task: Объект задачи под удаление.
    :param driver: Объект браузера.
    """

    # Получаем кнопку для отметки задачи.
    toggle_button = task.find_element_by_class_name("toggle")

    # Нажимаем на кнопку.
    driver.execute_script("arguments[0].click();", toggle_button)


def get_current_tasks_from_todo_list(driver, get_one_task=False):
    """Данная функция предназначена для получения
    всех задач из списка.

    :param driver: Объект браузера.
    :param get_one_task: Флаг, выставляемый в случае, когда нужно
                         получить не список задач, а одну задачу.
    :return Если выбран флаг get_one_task, то должна вернутся одна
            задача, которая будет встречена первой. Если флаг не выбран,
            то вернется список. Если задач в списке нет вообще, то список
            будет пустым.
    """

    # Находим список.
    todo_list = driver.find_element_by_class_name("todo-list")

    if get_one_task:
        # Вытягиваем первую попавшуюся запись в списке.
        task = todo_list.find_element_by_tag_name("li")
        return task
    else:
        # Вытягиваем из списка все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")
        return tasks


def get_completed_tasks_from_todo_list(driver, get_one_task=False):
    """Данная функция предназначена для получения
    всех 'выполненных' задач из списка.

    :param driver: Объект браузера.
    :param get_one_task: Флаг, выставляемый в случае, когда нужно
                         получить не список задач, а одну задачу.
    :return Если выбран флаг get_one_task, то должна вернутся одна
            задача, которая будет встречена первой. Если флаг не выбран,
            то вернется список. Если задач в списке нет вообще, то список
            будет пустым.
    """

    # Находим список.
    todo_list = driver.find_element_by_class_name("todo-list")

    if get_one_task:
        # Вытягиваем первую попавшуюся запись в списке.
        completed_task = todo_list.find_element_by_class_name("completed")
        return completed_task
    else:
        # Вытягиваем из списка все выполненные задачи.
        completed_tasks = todo_list.find_elements_by_class_name("completed")
        return completed_tasks


def clear_completed_tasks(driver):
    """Данная функция предназначена для очистки всех задач,
    помеченных как 'выполненные'.

    :param driver: Объект браузера.
    """

    # Обращаемся к footer'у списка.
    footer = driver.find_element_by_class_name("footer")
    # Получаем кнопку для удаления выполненных задач и нажимаем её.
    clear_completed_button = footer.find_element_by_class_name("clear-completed")
    driver.execute_script("arguments[0].click();", clear_completed_button)


def check_number_of_active_tasks(driver):
    """Данная функция предназначена для получения числа
    задач, не отмеченных как 'выполненные'.

    :param driver: Объект браузера.
    """

    # Находим число задач и проверяем их число.
    todo_count = driver.find_element_by_class_name("todo-count")
    number = int(todo_count.find_element_by_tag_name("strong").text)
    return number


@pytest.mark.parametrize("title, placeholder_text", (("React • TodoMVC", "What needs to be done?"),))
def test_opening_and_finding_input(browser, title, placeholder_text):
    """TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC

    Данный тест-кейс предназначен для проверки того, что приложение в
    принципе открывается в браузере при переходе по ссылке, а также
    то, что оно отрисует необходимый элемент для ввода задачи.
    """

    # Находим заголовок страницы и сравниваем с ожидаемым.
    page_title = browser.title
    assert page_title == title

    # Проверяем, что на странице есть элемент для ввода новой задачи.
    # и поле с текстом по умолчанию.
    # (Иначе, вылетает исключение NoSuchElementException)
    new_todo = browser.find_element_by_class_name("new-todo")
    placeholder = new_todo.get_attribute("placeholder")

    # Проверяем, что текст по умолчанию в поле для ввода соответствует ожидаемому.
    assert placeholder == placeholder_text


@pytest.mark.parametrize("task_name", ("Adding new task",))
def test_adding_task(browser, task_name):
    """TC ID: TodoMVC-1 - Добавить новую задачу

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить в поле для ввода название
    новой задачи, после чего она будет добавлена в список
    с тем же названием, которое ввел пользователь.
    """

    # Добавляем задачу.
    adding_task(task_name, browser)

    # Проверяем, что появилась задача.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Проверяем, что название задачи совпадает с введенным.
    name = task.find_element_by_tag_name("label").text
    assert name == task_name

    # Проверяем, что в нижней части формы появилась
    # панель для фильтрации и управления списком.
    footer = browser.find_element_by_class_name("footer")
    assert footer is not None


@pytest.mark.parametrize("task_names", (["Task 1", "Task 2"],))
def test_adding_task_to_non_empty_list(browser, task_names):
    """TC ID: TodoMVC-2 - Добавить новую задачу в непустой список

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить новую задачу в список, где
    задача уже была добавлена, и что в списке уже будет обе
    задачи.
    """

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Вытягиваем задачи, которые сейчас есть в списке.
    tasks = get_current_tasks_from_todo_list(browser)

    # Проверяем, что число полученных задач соответствует
    # длине списка с названиями задач.
    assert len(tasks) == len(task_names)

    # Проверяем, что названия задач в списке соответствуют тем,
    # которые были в списке изначально.
    for task in tasks:
        task_name = task.find_element_by_tag_name("label").text
        is_task_name_correct = task_name in task_names
        assert is_task_name_correct is True


@pytest.mark.parametrize("task_name", ("Delete this task",))
def test_delete_task(browser, task_name):
    """TC ID: TodoMVC-3 - Удалить задачу

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить задачу, а после этого
    удалить её из списка.
    """

    # Добавляем задачу.
    adding_task(task_name, browser)

    # Вытягиваем задачу.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Удаляем задачу.
    delete_task(task, browser)

    # Проверяем, что списка и подложки списка больше не существует.
    with pytest.raises(NoSuchElementException):
        browser.find_element_by_class_name("todo-list")
        browser.find_element_by_class_name("footer")


@pytest.mark.parametrize("task_for_deleting, task_for_saving", (("This must be deleted", "This must be saved"),))
def test_delete_task_from_non_empty_list(browser, task_for_deleting, task_for_saving):
    """TC ID: TodoMVC-4 - Удалить задачу из непустого списка.

    Данный тест-кейс предназначен для проверки того, что
    пользователь может добавить в список больше, чем одну
    задачу, а затем удалить одну конкретную из неё.
    """

    # Список задач.
    task_names = [task_for_deleting, task_for_saving]

    # Находим элемент для ввода новой задачи и записываем название.
    adding_task(task_names, browser)

    # Получаем список всех задач.
    tasks = get_current_tasks_from_todo_list(browser)

    # Перебираем все задачи, ищем ту, что нужно удалить.
    for task in tasks:
        label = task.find_element_by_tag_name("label").text

        # Если задача совпадает по имени, удаляем её:
        if label == task_for_deleting:
            delete_task(task, browser)

    # Снова вытягиваем задачи.
    tasks = get_current_tasks_from_todo_list(browser)
    # Проверяем, что длина списка стала меньше.
    assert len(tasks) + 1 == len(task_names)

    # Проверяем, что одна из задач осталась, а другая исчезла.
    is_task_saved = False
    for task in tasks:

        label = task.find_element_by_tag_name("label").text
        if label == task_for_saving:
            is_task_saved = True
        elif label == task_for_deleting:
            assert False

    assert is_task_saved is True


@pytest.mark.parametrize("task_name", ("This task will be marked as completed",))
def test_mark_task_as_completed(browser, task_name):
    """TC ID: TodoMVC-5 - Отметить задачу как 'выполненную'.

    Данный тест-кейс предназначен для проверки того, что
    задачу можно отметить как выполненную.
    """

    # Добавляем задачу.
    adding_task(task_name, browser)

    # Вытягиваем задачу.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Нажимаем на кнопку отметки задачи как выполненной.
    mark_task_as_completed(task, browser)

    # Проверяем, что в списке есть выполненная задача.
    assert get_completed_tasks_from_todo_list(browser, get_one_task=True)


@pytest.mark.parametrize("task_name", ("This task will be unmarked",))
def test_unmark_task_as_completed(browser, task_name):
    """TC ID: TodoMVC-6 - Снять отметку с 'выполненной' задачи.

    Данный тест-кейс предназначен для проверки того, что
    задачу можно отметить как выполненную и снять эту отметку.
    """

    # Добавляем задачу.
    adding_task(task_name, browser)

    # Получаем созданную задачу.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Дважды нажимаем на кнопку отметки задачи как выполненной.
    mark_task_as_completed(task, browser)
    mark_task_as_completed(task, browser)

    # Проверяем, что в списке нет выполненных задач.
    with pytest.raises(NoSuchElementException):
        browser.find_element_by_xpath("completed")


@pytest.mark.parametrize("task_names", (["Task 1", "Task 2"],))
def test_check_list_after_refresh(browser, task_names):
    """TC ID: TodoMVC-7 - Сохранение списка после обновления страницы

    Данный тест-кейс предназначен для проверки того, что
    пользователь может создать список, а затем обновить страницу
    и обнаружить, что список остался в том же виде.
    """

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Обновляем страницу.
    browser.refresh()

    # Находим список и проверяем, что он остался.
    tasks = get_current_tasks_from_todo_list(browser)
    assert tasks != []

    # Проверяем, что длина сохранилась.
    assert len(tasks) == len(task_names)

    # Проверяем, что имя каждой задачи есть в списке.
    for task in tasks:

        label = task.find_element_by_tag_name("label").text
        if label not in task_names:
            assert False


@pytest.mark.parametrize("old_task_name, new_task_name", (("Task before editing", "Task after editing"),))
def test_edit_name_of_task(browser, old_task_name, new_task_name):
    """TC ID: TodoMVC-8 - Отредактировать название задачи.

    Данный тест-кейс предназначен для проверки того, что
    пользователь сможет отредактировать название задачи,
    после чего она останется в списке уже с таким именем.
    """

    # Добавляем задачу.
    adding_task(old_task_name, browser)

    # Получаем созданную задачу.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Редактируем название задачи.
    edit_task_name(task, new_task_name, browser)

    # Снова получаем задачу и ее имя.
    task = get_current_tasks_from_todo_list(browser, get_one_task=True)

    # Проверяем, что текущее название задачи соответствует новому.
    assert task.find_element_by_tag_name("label").text == new_task_name


@pytest.mark.parametrize("task_for_deleting, task_for_saving", (("This must be deleted", "This must be saved"),))
def test_delete_completed_tasks(browser, task_for_deleting, task_for_saving):
    """TC ID: TodoMVC-9 - Удалить все 'выполненные' задачи

    Данный тест-кейс предназначен для проверки того, что
    пользователь может создать список, отметить задачу,
    а затем нажать на кнопку 'удалить все выполненные',
    и будет удалена только выполненная.
    """

    # Список названий задач.
    task_names = [task_for_deleting, task_for_saving]

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Получаем задачи.
    tasks = get_current_tasks_from_todo_list(browser)

    for task in tasks:

        label = task.find_element_by_tag_name("label").text

        if label == task_for_deleting:
            # Помечаем задачу как 'решенную'.
            mark_task_as_completed(task, browser)

    # Удаляем все 'выполненные' задачи.
    clear_completed_tasks(browser)

    # Проверяем, что одна из задач осталась, а другая исчезла.
    is_task_saved = False
    tasks = get_current_tasks_from_todo_list(browser)
    for task in tasks:

        label = task.find_element_by_tag_name("label").text
        if label == task_for_saving:
            is_task_saved = True
        elif label == task_for_deleting:
            assert False

    assert is_task_saved is True


@pytest.mark.parametrize("task_completed, task_active", (("This must not be shown", "This must be shown"),))
def test_show_only_not_completed_tasks(browser, task_completed, task_active):
    """TC ID: TodoMVC-10 - Показать только 'не выполненные' задачи.

    Данный тест-кейс предназначен для проверки того, что
    пользователь может создать список, отметить задачу,
    а затем нажать отфильтровать список, показав только
    'не выполненные задачи'.
    """

    # Список названий задач.
    task_names = [task_completed, task_active]

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Получаем задачи.
    tasks = get_current_tasks_from_todo_list(browser)

    # Перебираем все задачи по очереди.
    for task in tasks:

        label = task.find_element_by_tag_name("label").text

        if label == task_completed:
            # Помечаем задачу как 'решенную'.
            mark_task_as_completed(task, browser)

    # Обращаемся только к не завершенным задачам.
    browser.get("http://todomvc.com/examples/react/#/active")

    # Проверяем, что одна из задач осталась, а другая исчезла.
    tasks = get_current_tasks_from_todo_list(browser)
    is_task_saved = False
    for task in tasks:

        label = task.find_element_by_tag_name("label").text
        if label == task_active:
            is_task_saved = True
        elif label == task_completed:
            assert False

    assert is_task_saved is True


@pytest.mark.parametrize("task_completed, task_active", (("This must be shown", "This must not be shown"),))
def test_show_only_completed_tasks(browser, task_completed, task_active):
    """TC ID: TodoMVC-11 - Показать только 'выполненные' задачи.

    Данный тест-кейс предназначен для проверки того, что
    пользователь может создать список, отметить задачу,
    а затем нажать отфильтровать список, показав только
    'выполненные задачи'.
    """

    # Список названий задач.
    task_names = [task_completed, task_active]

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Получаем задачи.
    tasks = get_current_tasks_from_todo_list(browser)

    # Перебираем все задачи по очереди.
    for task in tasks:

        label = task.find_element_by_tag_name("label").text

        if label == task_completed:
            # Помечаем задачу как 'решенную'.
            mark_task_as_completed(task, browser)

    # Обращаемся только к не завершенным задачам.
    browser.get("http://todomvc.com/examples/react/#/completed")

    # Проверяем, что одна из задач осталась, а другая исчезла.
    is_task_saved = False

    tasks = get_current_tasks_from_todo_list(browser)
    for task in tasks:

        label = task.find_element_by_tag_name("label").text
        if label == task_completed:
            is_task_saved = True
        elif label == task_active:
            assert False

    assert is_task_saved is True


@pytest.mark.parametrize("task_completed, task_active", (("This task is completed", "This task is active"),))
def test_check_amount_of_active_tasks(browser, task_completed, task_active):
    """TC ID: TodoMVC-12 - Проверить количество 'не выполненных задач'.

    Данный тест-кейс предназначен для проверки того, что
    пользователь может узнать количество 'не выполненных задач'
    по строке в подложке списка.
    """

    # Список названий задач.
    task_names = [task_completed, task_active]

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Находим число задач и проверяем их число.
    assert check_number_of_active_tasks(browser) == 2

    # Получаем задачи.
    tasks = get_current_tasks_from_todo_list(browser)
    for task in tasks:

        label = task.find_element_by_tag_name("label").text

        if label == task_completed:
            # Помечаем задачу как 'решенную'.
            mark_task_as_completed(task, browser)

    # Находим число задач и проверяем их число.
    assert check_number_of_active_tasks(browser) == 1


@pytest.mark.parametrize("task_names", (["Task 1", "Task 2"],))
def test_mark_all_tasks_as_completed(browser, task_names):
    """TC ID: TodoMVC-13 - Отметить все задачи как 'выполненные'.

    Данный тест-кейс предназначен для проверки того, что
    пользователь может разом отметить все задачи как
    'выполненные'.
    """

    # Добавляем задачи.
    adding_task(task_names, browser)

    # Находим кнопку для отметки всех задач как 'выполненные' и нажимаем её.
    toggle_all = browser.find_element_by_class_name("toggle-all")
    browser.execute_script("arguments[0].click();", toggle_all)

    # Получаем все выполненные задачи.
    completed_tasks = get_completed_tasks_from_todo_list(browser)
    assert completed_tasks is not None

    # Проверяем, что их число соответствует числу созданных.
    assert len(completed_tasks) == len(task_names)

    # Проверяем, что их имена соответствуют заданным ранее.
    for task in completed_tasks:

        label = task.find_element_by_tag_name("label").text
        if label not in task_names:
            assert False
