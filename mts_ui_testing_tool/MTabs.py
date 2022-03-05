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
            print("\n'm-tabs' - элемент найден")

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент 'm-tabs'")

    # def click_tab_by_index(self, tab_index: int) -> None:
    #     """При вызове данного метода происходит клик по табу исходя из его индекса (начиная с 1)"""
    #     # TODO add an exception in case tab is disabled?
    #     inner_tab = self.m_tab.find_element(By.CSS_SELECTOR,
    #                                    f"div:first-child > div:nth-child(2) > nav > div:nth-child({tab_index})")
    #     inner_tab.click()

    # def check_if_tab_is_enabled_by_index(self, tab_index: int) -> bool:
    #     """
    #     Данный метод найдет таб по индексу и вернет булево значение в зависимости от статуса таба:
    #     True если enabled и False если таб имеет состояние disabled
    #     """
    #     inner_tab = self.m_tab.find_element(By.CSS_SELECTOR,
    #                                         f"div:first-child > div:nth-child(2) > nav > div:nth-child({tab_index})")
    #     return inner_tab.is_enabled()

    def click_tab_by_text(self, tab_text: str) -> None:
        # TODO EXCEPTIONS таба нет вообще
        self.m_tab.find_element(By.CSS_SELECTOR, f"[data-test-id={tab_text}-tab-nav]").click()

    def check_if_tab_is_enabled_by_text(self, tab_text: str) -> bool:
        """
        Данный метод найдет таб по тексту и вернет булево значение в зависимости от статуса таба:
        True если enabled и False если таб имеет состояние disabled
        """
        # TODO EXCEPTIONS таба нет вообще
        inner_tab = self.m_tab.find_element(By.CSS_SELECTOR, f"[data-test-id={tab_text}-tab-nav]")
        return inner_tab.isEnabled()

    def check_if_tab_content_is_loaded_by_text(self, tab_text, waiting_time):
        # TODO Как обработать ситуацию, когда таб не был кликнут? Проверить сперва статус таба и потом кинуть ошибку?
        try:
            self.m_tab = WebDriverWait(self.browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={tab_text}-tab-content]")
                )
            )
            print("\nf'Контент для таба с текстом {tab_text} не был найден")

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент 'm-tabs'")

    # TODO Вынести поиск табов отдельно?
    # def _private_function_that_finds_tabs
