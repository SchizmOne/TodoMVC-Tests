import os
import pytest
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class TestFirefox:
    """Данный набор тестов предназначен для запуска
    автоматических тестов в Google Chrome.
    """

    browser = None
    if os.name == "nt":
        PATH_TO_WEBDRIVER = os.path.join(os.getcwd(), "webdrivers", "geckodriver.exe")
    else:
        PATH_TO_WEBDRIVER = os.path.join(os.getcwd(), "webdrivers", "geckodriver")

    def setup_class(self):
        """Метод, предназначенный для запуска всего класса,
        запускающий браузер и устанавливающий его настройки.
        """

        # Запускаем Geckodriver.
        self.browser = Firefox(executable_path=self.PATH_TO_WEBDRIVER)

        # Выставляем время, которое будет дано браузеру, чтобы найти элементы
        # или завершить какую-либо операцию.
        self.browser.implicitly_wait(3)

    def setup_method(self):
        """Метод, предназначенный для подготовки
        каждого из тестов.
        """

        # Ссылка на TodoMVC
        url = "http://todomvc.com/examples/react/"
        # Открываем TodoMVC в браузере.
        self.browser.get(url)

    def teardown_method(self):
        """Метод, предназначенный для завершения работы
        любого из тестов.
        """

        # Чистим локальное хранилище со списком.
        self.browser.execute_script("window.localStorage.clear();")
        # Обновить страницу, чтобы гарантировать чистку.
        self.browser.refresh()

    def teardown_class(self):
        """Метод, предназначенный для завершения работы
        тестов в рамках класса.
        """

        # Закрываем страницу.
        self.browser.close()
        # Закрываем браузер.
        self.browser.quit()

    def test_opening_and_finding_input(self):
        """TC ID: TodoMVC-0 - Доступ и отображение начальной страницы TodoMVC

        Данный тест-кейс предназначен для проверки того, что приложение в
        принципе открывается в браузере при переходе по ссылке, а также
        то, что оно отрисует необходимый элемент для ввода задачи.
        """

        # Ожидаемый заголовок страницы.
        title = "React • TodoMVC"
        # Ожидаемый текст по умолчанию в поле для ввода.
        placeholder_text = "What needs to be done?"

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

        # Текст с названием задачи.
        new_task_name = "TC ID: TodoMVC-1 - Добавить новую задачу"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(new_task_name + Keys.ENTER)

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

        # Список названий задач.
        task_names = ["Задача 1", "Задача 2"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for new_task in task_names:
            new_todo.send_keys(new_task, Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")

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

        # Текст с названием задачи.
        task_name = "Задача под удаление"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(task_name + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него задачу.
        task = todo_list.find_element_by_tag_name("li")

        # Нажимаем на кнопку удаления задачи.
        #
        # (Примечание: Видимо, click() обычный не работает, когда
        # кнопка отображается только при наведении курсора. StackOverflow
        # подсказывает, что это проблема Selenium и советует использовать
        # готовый JS-код для клика на кнопки в таких ситуациях.
        destroy_button = task.find_element_by_class_name("destroy")
        self.browser.execute_script("arguments[0].click();", destroy_button)

        # Проверяем, что списка и подложки списка больше не существует.
        with pytest.raises(NoSuchElementException):
            self.browser.find_element_by_class_name("todo-list")
            self.browser.find_element_by_class_name("footer")

    def test_delete_task_from_non_empty_list(self):
        """TC ID: TodoMVC-4 - Удалить задачу из непустого списка.

        Данный тест-кейс предназначен для проверки того, что
        пользователь может добавить в список больше, чем одну
        задачу, а затем удалить одну конкретную из неё.
        """

        # Тексты с названиями задач.
        task_names = ["Эта задача под удаление", "Эта задача должна остаться"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")

        for task in tasks:

            label = task.find_element_by_tag_name("label").text

            if label == "Эта задача под удаление":
                # Нажимаем на кнопку удаления задачи.
                destroy_button = task.find_element_by_class_name("destroy")
                self.browser.execute_script("arguments[0].click();", destroy_button)

        # Снова вытягиваем задачи.
        tasks = todo_list.find_elements_by_tag_name("li")
        # Проверяем, что длина списка стала меньше.
        assert len(tasks) + 1 == len(task_names)

        # Проверяем, что одна из задач осталась, а другая исчезла.
        is_task_saved = False
        for task in tasks:

            label = task.find_element_by_tag_name("label").text
            if label == "Эта задача должна остаться":
                is_task_saved = True
            elif label == "Эта задача под удаление":
                assert False

        assert is_task_saved is True

    def test_mark_task_as_completed(self):
        """TC ID: TodoMVC-5 - Отметить задачу как 'выполненную'.

        Данный тест-кейс предназначен для проверки того, что
        задачу можно отметить как выполненную.
        """

        # Текст с названием задачи.
        task_name = "Эта задача будет завершена"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(task_name + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него задачу.
        task = todo_list.find_element_by_tag_name("li")

        # Нажимаем на кнопку отметки задачи как выполненной.
        toggle_button = task.find_element_by_class_name("toggle")
        self.browser.execute_script("arguments[0].click();", toggle_button)

        # Проверяем, что в списке есть выполненная задача.
        completed_task = todo_list.find_element_by_class_name("completed")
        assert completed_task is not None

    def test_unmark_task_as_completed(self):
        """TC ID: TodoMVC-6 - Снять отметку с 'выполненной' задачи.

        Данный тест-кейс предназначен для проверки того, что
        задачу можно отметить как выполненную и снять эту отметку.
        """

        # Текст с названием задачи.
        task_name = "Эта задача будет завершена и открыта снова"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(task_name + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него задачу.
        task = todo_list.find_element_by_tag_name("li")

        # Нажимаем на кнопку отметки задачи как выполненной.
        toggle_button = task.find_element_by_class_name("toggle")
        self.browser.execute_script("arguments[0].click();", toggle_button)
        # И нажимаем на кнопку еще раз.
        self.browser.execute_script("arguments[0].click();", toggle_button)

        # Проверяем, что в списке нет выполненных задач.
        with pytest.raises(NoSuchElementException):
            self.browser.find_element_by_xpath("completed")

    def test_check_list_after_refresh(self):
        """TC ID: TodoMVC-7 - Сохранение списка после обновления страницы

        Данный тест-кейс предназначен для проверки того, что
        пользователь может создать список, а затем обновить страницу
        и обнаружить, что список остался в том же виде.
        """

        # Список названий задач.
        task_names = ["Задача 1", "Задача 2"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for new_task in task_names:
            new_todo.send_keys(new_task, Keys.ENTER)

        # Обновляем страницу.
        self.browser.refresh()

        # Находим список и проверяем, что он остался.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        tasks = todo_list.find_elements_by_tag_name("li")
        assert tasks is not None

        # Проверяем, что длина сохранилась.
        assert len(tasks) == len(task_names)

        # Проверяем, что имя каждой задачи есть в списке.
        for task in tasks:

            label = task.find_element_by_tag_name("label").text
            if label not in task_names:
                assert False

    def test_edit_name_of_task(self):
        """TC ID: TodoMVC-8 - Отредактировать название задачи.

        Данный тест-кейс предназначен для проверки того, что
        пользователь сможет отредактировать название задачи,
        после чего она останется в списке уже с таким именем.
        """

        # Текст с названием задачи.
        old_task_name = "Название задачи до редактирования"
        new_task_name = "Название задачи после редактирования"

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        new_todo.send_keys(old_task_name + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него задачу.
        task = todo_list.find_element_by_tag_name("li")

        # Дважды кликаем на название задачи, чтобы она стала редактируемой.
        view = task.find_element_by_class_name("view")
        action_chains = ActionChains(self.browser)
        action_chains.double_click(view).perform()

        # Повторно вытягиваем задачу в режиме редактирования.
        edit_input = task.find_element_by_class_name("edit")
        # По очереди стираем все название до этого.
        for _ in old_task_name:
            edit_input.send_keys(Keys.BACK_SPACE)
        # Вводим новое название.
        edit_input.send_keys(new_task_name, Keys.ENTER)

        # Снова получаем задачу.
        task = todo_list.find_element_by_tag_name("li")
        label = task.find_element_by_tag_name("label").text

        # Проверяем, что текущее название задачи соответствует новому.
        assert label == new_task_name

    def test_delete_completed_tasks(self):
        """TC ID: TodoMVC-9 - Удалить все 'выполненные' задачи

        Данный тест-кейс предназначен для проверки того, что
        пользователь может создать список, отметить задачу,
        а затем нажать на кнопку 'удалить все выполненные',
        и будет удалена только выполненная.
        """

        # Список названий задач.
        task_names = ["Эта задача под удаление", "Эта задача должна остаться"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")

        for task in tasks:

            label = task.find_element_by_tag_name("label").text

            if label == "Эта задача под удаление":
                # Помечаем задачу как 'решенную'.
                toggle_button = task.find_element_by_class_name("toggle")
                self.browser.execute_script("arguments[0].click();", toggle_button)

        # Обращаемся к footer'у списка.
        footer = self.browser.find_element_by_class_name("footer")
        # Получаем кнопку для удаления выполненных задач и нажимаем её.
        clear_completed_button = footer.find_element_by_class_name("clear-completed")
        self.browser.execute_script("arguments[0].click();", clear_completed_button)

        # Проверяем, что одна из задач осталась, а другая исчезла.
        is_task_saved = False

        tasks = todo_list.find_elements_by_tag_name("li")
        for task in tasks:

            label = task.find_element_by_tag_name("label").text
            if label == "Эта задача должна остаться":
                is_task_saved = True
            elif label == "Эта задача под удаление":
                assert False

        assert is_task_saved is True

    def test_show_only_not_completed_tasks(self):
        """TC ID: TodoMVC-10 - Показать только 'не выполненные' задачи.

        Данный тест-кейс предназначен для проверки того, что
        пользователь может создать список, отметить задачу,
        а затем нажать отфильтровать список, показав только
        'не выполненные задачи'.
        """

        # Список названий задач.
        task_names = ["Эта задача будет выполнена", "Эта задача не будет выполнена"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")

        for task in tasks:

            label = task.find_element_by_tag_name("label").text

            if label == "Эта задача будет выполнена":
                # Помечаем задачу как 'решенную'.
                toggle_button = task.find_element_by_class_name("toggle")
                self.browser.execute_script("arguments[0].click();", toggle_button)

        # Обращаемся только к не завершенным задачам.
        self.browser.get("http://todomvc.com/examples/react/#/active")

        # Проверяем, что одна из задач осталась, а другая исчезла.
        is_task_saved = False

        tasks = todo_list.find_elements_by_tag_name("li")
        for task in tasks:

            label = task.find_element_by_tag_name("label").text
            if label == "Эта задача не будет выполнена":
                is_task_saved = True
            elif label == "Эта задача будет выполнена":
                assert False

        assert is_task_saved is True

    def test_show_only_completed_tasks(self):
        """TC ID: TodoMVC-11 - Показать только 'выполненные' задачи.

        Данный тест-кейс предназначен для проверки того, что
        пользователь может создать список, отметить задачу,
        а затем нажать отфильтровать список, показав только
        'выполненные задачи'.
        """

        # Список названий задач.
        task_names = ["Эта задача будет выполнена", "Эта задача не будет выполнена"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")

        for task in tasks:

            label = task.find_element_by_tag_name("label").text

            if label == "Эта задача будет выполнена":
                # Помечаем задачу как 'решенную'.
                toggle_button = task.find_element_by_class_name("toggle")
                self.browser.execute_script("arguments[0].click();", toggle_button)

        # Обращаемся только к не завершенным задачам.
        self.browser.get("http://todomvc.com/examples/react/#/completed")

        # Проверяем, что одна из задач осталась, а другая исчезла.
        is_task_saved = False

        tasks = todo_list.find_elements_by_tag_name("li")
        for task in tasks:

            label = task.find_element_by_tag_name("label").text
            if label == "Эта задача будет выполнена":
                is_task_saved = True
            elif label == "Эта задача не будет выполнена":
                assert False

        assert is_task_saved is True

    def test_check_amount_of_active_tasks(self):
        """TC ID: TodoMVC-12 - Проверить количество 'не выполненных задач'.

        Данный тест-кейс предназначен для проверки того, что
        пользователь может узнать количество 'не выполненных задач'
        по строке в подложке списка.
        """

        # Список названий задач.
        task_names = ["Эта задача будет выполнена", "Эта задача не будет выполнена"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим число задач и проверяем их число.
        todo_count = self.browser.find_element_by_class_name("todo-count")
        number = int(todo_count.find_element_by_tag_name("strong").text)
        assert number == 2

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все задачи.
        tasks = todo_list.find_elements_by_tag_name("li")

        for task in tasks:

            label = task.find_element_by_tag_name("label").text

            if label == "Эта задача будет выполнена":
                # Помечаем задачу как 'решенную'.
                toggle_button = task.find_element_by_class_name("toggle")
                self.browser.execute_script("arguments[0].click();", toggle_button)

        # Находим число задач и проверяем их число.
        todo_count = self.browser.find_element_by_class_name("todo-count")
        number = int(todo_count.find_element_by_tag_name("strong").text)
        assert number == 1

    def test_mark_all_tasks_as_completed(self):
        """TC ID: TodoMVC-13 - Отметить все задачи как 'выполненные'.

        Данный тест-кейс предназначен для проверки того, что
        пользователь может разом отметить все задачи как
        'выполненные'.
        """

        # Список названий задач.
        task_names = ["Эта задача будет выполнена", "Эта задача тоже будет выполнена"]

        # Находим элемент для ввода новой задачи и записываем название.
        new_todo = self.browser.find_element_by_class_name("new-todo")
        for task in task_names:
            new_todo.send_keys(task + Keys.ENTER)

        # Находим кнопку для отметки всех задач как 'выполненные' и нажимаем её.
        toggle_all = self.browser.find_element_by_class_name("toggle-all")
        self.browser.execute_script("arguments[0].click();", toggle_all)

        # Находим список.
        todo_list = self.browser.find_element_by_class_name("todo-list")
        # Вытягиваем из него все 'выполненные' задачи и проверяем, что они есть.
        completed_tasks = todo_list.find_elements_by_class_name("completed")
        assert completed_tasks is not None

        # Проверяем, что их число соответствует числу созданных.
        assert len(completed_tasks) == len(task_names)

        # Проверяем, что их имена соответствуют заданным ранее.
        for task in completed_tasks:

            label = task.find_element_by_tag_name("label").text
            if label not in task_names:
                assert False
