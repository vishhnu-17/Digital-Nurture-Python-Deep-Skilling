from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pytest

@pytest.mark.parametrize(
    "message",
    [
        "Hello",
        "Selenium Automation",
        "12345"
    ]
)


def test_simple_form_submission(driver, message, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
    driver.find_element(By.ID, "user-message").send_keys(message)

    time.sleep(5)
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "showInput"))
    )
    button.click()
    if WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element(
        (By.ID, "message"),
        message
    )):
        output=driver.find_element(By.ID,"message")

    print(f"Message displayed: {output.text}")
    assert output.text == message


def test_checkbox_interaction(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT,"Checkbox Demo").click()
    checkbox=driver.find_element(By.XPATH,'//*[@id="__next"]/div/main/div/section/div/div/div[1]/label/input')
    
    checkbox.click()
    assert checkbox.is_selected()

    checkbox.click()
    assert not checkbox.is_selected()

def test_dropdown_selection(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT,"Select Dropdown List").click()
    dropdown=Select(driver.find_element(By.ID, "select-demo"))
    dropdown.select_by_visible_text("Wednesday")
    assert (dropdown.first_selected_option.text=="Wednesday")





