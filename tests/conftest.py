import os
import pytest
import selenium.webdriver.chrome.options
import selenium.webdriver.firefox.options
from selenium.webdriver import Firefox, Chrome


# Путь к папке с вебдрайверами.
PATH_TO_WEBDRIVER = os.path.join(os.getcwd(), "webdrivers")
# Ссылка на TodoMVC.
URL = "http://todomvc.com/examples/react/"


def pytest_addoption(parser):
    """Здесь задаются дополнительные аргументы для
    прогона тестов, запускаемого из командной строки.
    """
    parser.addoption('--browser',
                     default='firefox',
                     help='option to choose name of browser')
    parser.addoption('--headless',
                     action="store_true",
                     help='option to run browser without UI')


@pytest.fixture(scope="session")
def browser(request):
    """Возвращает сгенерированный объект 'браузер'
    для дальнейшей работы с ним в тестах. А в конце
    тестовой сессии закрывает его.
    """
    # Получаем аргумент с названием браузера.
    browser_name = request.config.getoption('--browser')

    # Если выбран в качестве браузера Chrome:
    if browser_name.lower() == "chrome":
        chrome_options = selenium.webdriver.chrome.options.Options()
        chrome_options.add_argument("log-level=CRITICAL")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Если тесты запущены в headless режиме.
        if request.config.getoption("--headless"):
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        driver = Chrome(executable_path=os.path.join(PATH_TO_WEBDRIVER, "chromedriver"), options=chrome_options)

    # Если выбран в качестве браузера Firefox
    elif browser_name.lower() == "firefox":
        firefox_options = selenium.webdriver.firefox.options.Options()

        # Если тесты запущены в headless режиме.
        if request.config.getoption("--headless"):
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--disable-gpu")

        driver = Firefox(executable_path=os.path.join(PATH_TO_WEBDRIVER, "geckodriver"), options=firefox_options,
                         service_log_path=os.path.devnull)

    # Если ни один из них, то возвращаем ошибку.
    else:
        pytest.fail("Tests for browser '{}' are not implemented.".format(browser_name))
        return

    # Выставляем время, которое будет дано браузеру, чтобы найти элементы
    # или завершить какую-либо операцию.
    driver.implicitly_wait(3)

    # Возвращаем объект браузера в вызывающие его тестовые функции.
    yield driver

    # Как только все тесты завершены, то переходим к этой части кода.
    def browser_fin():
        """Функция для завершения работы в тест-сессии.
        Закрываем вкладку и сам браузер.
        """
        print("\nQuiting the Browser...")
        driver.close()
        driver.quit()

    # Добавляем функцию выше как finalizer.
    request.addfinalizer(browser_fin)


@pytest.fixture(scope="function", autouse=True)
def setup_test(request, browser):
    """Данная фикстура предназначена для вызова в начале
    каждого теста. В ней мы переходим по адресу приложения
    TodoMVC.
    """

    print("\nStarting new test...")
    # Открываем TodoMVC в браузере.
    browser.get(URL)

    def teardown_test():
        """Данная функция автоматически вызывается в конце работы
        каждого теста. Здесь производится чистка локального хранилища
        и обновление страницы, чтобы подготовить все, так будто оно
        'запущено в первый раз'.
        """
        print("\nClearing page after test...")
        browser.execute_script("window.localStorage.clear();")
        browser.refresh()

    # Добавляем функцию для автоматической очистки local storage после
    # каждого теста.
    request.addfinalizer(teardown_test)
