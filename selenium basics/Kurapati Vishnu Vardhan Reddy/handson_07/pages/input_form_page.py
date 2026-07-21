from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from pages.base_page import BasePage


class InputFormPage(BasePage):

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "inputEmail4")
    PASSWORD = (By.ID, "inputPassword4")
    COMPANY = (By.ID, "company")
    WEBSITE = (By.ID, "websitename")

    COUNTRY = (By.NAME, "country")

    ADDRESS1 = (By.ID, "inputAddress1")
    ADDRESS2 = (By.ID, "inputAddress2")
    CITY = (By.ID, "inputCity")
    STATE = (By.ID, "inputState")
    ZIPCODE = (By.ID, "inputZip")

    SUBMIT_BUTTON = (
    By.CSS_SELECTOR,
    "#seleniumform button[type='submit']"
)

    SUCCESS_MESSAGE = (By.XPATH,
    "//p[contains(@class,'success-msg') and contains(text(),'Thanks for contacting us')]")

    def fill_form(
        self,
        name,
        email,
        password,
        company,
        website,
        address1,
        address2,
        city,
        state,
        country,
        zipcode,
    ):

        self.wait_for_element(self.NAME).send_keys(name)
        self.wait_for_element(self.EMAIL).send_keys(email)
        self.wait_for_element(self.PASSWORD).send_keys(password)
        self.wait_for_element(self.COMPANY).send_keys(company)
        self.wait_for_element(self.WEBSITE).send_keys(website)

        Select(
            self.wait_for_element(self.COUNTRY)
        ).select_by_visible_text(country)

        self.wait_for_element(self.ADDRESS1).send_keys(address1)
        self.wait_for_element(self.ADDRESS2).send_keys(address2)
        self.wait_for_element(self.CITY).send_keys(city)
        self.wait_for_element(self.STATE).send_keys(state)
        self.wait_for_element(self.ZIPCODE).send_keys(zipcode)

    from selenium.webdriver.common.action_chains import ActionChains
    import time

    def submit_form(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SUBMIT_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        time.sleep(1)

        self.driver.execute_script(
            "arguments[0].click();",
            button
        )

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_MESSAGE).text