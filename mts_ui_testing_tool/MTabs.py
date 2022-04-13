from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class MTabs:
    """
    Этот класс делает что-то полезное с табами

    Использование: m_tab = MTabs(path_to_tab, waiting_time, browser)

    Аргументы: path - путь к элементу, waiting_time - время ожидания, по умолчанию равно 2,
    browser = текущая сессия WebDriver

    Ошибки: TimeoutException, ElementNotFoundException

    Возвращает:
    """

    def __init__(self, path: str, waiting_time=2, browser=webdriver.Chrome()):
        self.browser = browser
        self.m_tab = None

        try:
            self.m_tab = WebDriverWait(browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, path)
                )
            )

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент 'm-tabs'")

    def click_tab_by_data_test_id(self, data_test_id: str) -> None:
        # TODO EXCEPTIONS если таба нет вообще
        self.m_tab.find_element(By.CSS_SELECTOR, f"[data-test-id={data_test_id}]").click()

    def check_if_tab_is_enabled_by_data_test_id(self, data_test_id: str) -> bool:
        """
        Данный метод найдет таб по data-test-id и вернет булево значение в зависимости от статуса таба:
        True если таб имеет состояние enabled и False если таб имеет состояние disabled
        """
        # TODO EXCEPTIONS если таба нет вообще
        element = self.m_tab.find_element(By.CSS_SELECTOR, f"[data-test-id={data_test_id}]")
        return element.is_enabled()

    def check_if_tab_content_is_loaded_by_test_id(self, data_test_id: str, waiting_time=2) -> bool:
        tab_content = None
        try:
            tab_content = WebDriverWait(self.browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={data_test_id}]")
                )
            )
            return bool(tab_content)

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти таб с контентом.")
