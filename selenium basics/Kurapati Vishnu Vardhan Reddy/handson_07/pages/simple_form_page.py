from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time


class SimpleFormPage(BasePage):
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")
    DISPLAY_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        self.wait_for_element(self.MESSAGE_INPUT).clear()
        self.wait_for_element(self.MESSAGE_INPUT).send_keys(text)

    def click_submit(self):
        # LambdaTest sometimes delays JS initialization
        time.sleep(1)
        self.wait_until_clickable(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAY_MESSAGE).text