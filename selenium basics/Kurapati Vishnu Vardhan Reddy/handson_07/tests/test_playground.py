import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url + "simple-form-demo")
    page.enter_message("Hello Selenium")
    page.click_submit()
    assert page.get_displayed_message() == "Hello Selenium"


def test_checkbox_demo(driver, base_url):
    page = CheckboxPage(driver)
    page.navigate_to(base_url + "checkbox-demo")
    page.check_option(0)
    assert page.is_option_checked(0)
    page.uncheck_option(0)
    assert not page.is_option_checked(0)


def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)
    page.navigate_to(base_url + "select-dropdown-demo")
    page.select_day("Wednesday")
    assert page.get_selected_day() == "Wednesday"


def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)
    page.navigate_to(base_url + "input-form-demo")
    page.fill_form(
        "Cynthia",
        "cynthia@test.com",
        "Password123",
        "OpenAI",
        "www.openai.com",
        "123 Anna Salai",
        "Near Central Station",
        "Chennai",
        "Tamil Nadu",
        "United States",
        "600001"
    )
    page.submit_form()
    assert (page.get_success_message() == 
            "Thanks for contacting us, we will get back to you shortly.")

