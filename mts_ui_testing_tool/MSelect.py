import time
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException


# TODO добавить поиск элемента по data-test-id
# TODO использовать основу some-select как путь
# QSN локатор должен передаваться в виде tuple? Будут ли другие способы передачи path кроме data-test-id?
class MSelect:
    def __init__(self, browser: Remote, input_data_test_id: str, select_dropdown_data_test_id: str, waiting_time=2):
        self.browser = browser
        self.select_dropdown = None
        self.input = None

        try:
            self.input = WebDriverWait(browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={input_data_test_id}]")
                )
            )

            self.select_dropdown = WebDriverWait(browser, waiting_time).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f"[data-test-id={select_dropdown_data_test_id}]")
                )
            )

        except TimeoutException:
            raise TimeoutException(f"\nПосле {waiting_time} секунд ожидания не удалось найти элемент '???'")

    def toggle_dropdown(self) -> None:
        self.input.click()

    def is_element_present(self, text) -> bool:
        pass

    # QSN что делать если в начале и в конце лишний пробел? надо тримить перед передачей в инпут?
    def __search_select_dropdown(self, search_value: str) -> WebElement | None:
        select_dropdown_elements: [WebElement] = self.select_dropdown.find_elements(By.CSS_SELECTOR, ".m-select-item")
        for el in select_dropdown_elements:
            if el.text == search_value:
                return el
        return None

    # TODO принимать отдельную функцию для сравнения в find_element_by_text, функция должна работаьт на подобие функций sort

    # TODO Сделать отдельно скролл, поиск по новым подгруженным элементам и поиск по разным свойствам (substring?)
    # TODO Сделать метод-предикат, или достаточно этого, просто assert not false пусть делают?
    def find_element_by_text(self, search_value: str) -> WebElement | bool:
        self.toggle_dropdown()
        # TODO ожидание загрузки страницы? Точнее, ожидание конкретного элемента?
        time.sleep(1)
        # TODO передать строку для поиска в input
        self.input.send_keys(search_value)
        num_of_pixels_to_scroll = 0
        vertical_offset = 0
        # TODO Надо скроллить с большим шагом? Давать ли возможность задать шаг скролла?
        while num_of_pixels_to_scroll <= vertical_offset:
            element = self.__search_select_dropdown(search_value)
            if element:
                print("\nЭлемент найден")
                return element
            else:
                num_of_pixels_to_scroll += 300
                self.browser.execute_script("arguments[0].scrollTo(0, arguments[1])", self.select_dropdown,
                                            num_of_pixels_to_scroll)
                # TODO Подождать, надо как-то понять, что очередная порция данных подгрузилась
                time.sleep(2)
                vertical_offset = self.browser.execute_script("return arguments[0].scrollTop", self.select_dropdown)
        print("\nСкролить некуда, элемент не был найден")
        return False
        # TODO Кинуть исключение?
