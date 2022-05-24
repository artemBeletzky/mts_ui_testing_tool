from selenium.webdriver.remote.webelement import WebElement


class MTab:
    def __init__(self, element: WebElement):
        self.tab = element

    def click(self) -> None:
        self.tab.click()

    def is_enabled(self) -> bool:
        return self.tab.is_enabled()
