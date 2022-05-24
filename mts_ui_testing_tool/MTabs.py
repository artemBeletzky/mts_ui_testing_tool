from selenium.webdriver import Remote
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .MTab import MTab
from .common.custom_exceptions import TabNotFound


class MTabs:
    """
    Этот класс делает что-то полезное с табами

    Использование: contacts_tab = MTabs(path_to_contacts_tab, waiting_time, browser)

    Аргументы: path_to_contacts_tab - путь к элементу, waiting_time - время ожидания (по умолчанию равно 2 секундам),
    browser = текущая сессия WebDriver

    Ошибки: TimeoutException, NoSuchElementException

    Возвращает:
    """

    def __init__(self, path: str, browser: Remote, waiting_time=2):
        self.browser = browser
        self.m_tabs = None

        try:
            self.m_tabs = WebDriverWait(browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, path)
                )
            )

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент 'm-tabs'")

    def __find_tab(self, data_test_id: str) -> WebElement:
        try:
            tab = self.m_tabs.find_element(By.CSS_SELECTOR, f"[data-test-id={data_test_id}]")
        except NoSuchElementException:
            # raise TabNotFound(f"Не удалось найти таб с data_test_id '{data_test_id}'")
            raise NoSuchElementException(f"\nНе удалось найти таб с data_test_id '{data_test_id}'")
        return tab

    def __find_tab_using_wait(self, data_test_id: str, waiting_time=2) -> WebElement:
        try:
            tab = WebDriverWait(self.browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={data_test_id}]")
                )
            )
        except TimeoutException:
            raise TimeoutException(
                f"\nПосле {waiting_time} секунд ожидания, не удалось найти таб с data_test_id '{data_test_id}'.")
        except NoSuchElementException:
            raise NoSuchElementException(f"\nНе удалось найти таб с data_test_id '{data_test_id}'")
        return tab

    def click_tab_by_data_test_id(self, data_test_id: str) -> None:
        tab = MTab(self.__find_tab(data_test_id))
        tab.click()

    def check_if_tab_is_enabled_by_data_test_id(self, data_test_id: str) -> bool:
        """
        Данный метод найдет таб по data-test-id и вернет булево значение в зависимости от статуса таба:
        True если таб имеет состояние enabled и False если таб имеет состояние disabled
        """
        tab: WebElement = self.__find_tab(data_test_id)
        return tab.is_enabled()

    def check_if_tab_content_is_loaded_by_test_id(self, data_test_id: str, waiting_time=2) -> bool:
        try:
            tab_content = WebDriverWait(self.browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={data_test_id}]")
                )
            )
            return bool(tab_content)

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти таб с контентом.")
