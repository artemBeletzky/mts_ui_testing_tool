from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class MCounter:
    def __init__(self, path: str, waiting_time=2, browser=webdriver.Chrome()):
        self.browser = browser
        self.m_counter = None

        try:
            self.m_counter = WebDriverWait(browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, path)
                )
            )

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент 'm-counter'")

    def check_if_current_count_is_equal_to(self, count_to_compare: int) -> bool:
        current_count = self.m_counter.find_element(By.CSS_SELECTOR, "p").text
        return int(current_count) == count_to_compare
