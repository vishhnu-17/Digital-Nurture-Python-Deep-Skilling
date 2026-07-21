from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get("https://www.lambdatest.com/selenium-playground/")
driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
assert "simple-form-demo" in driver.current_url
driver.back()


driver.execute_script(
    'window.open("https://www.google.com");'
)
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[1])
print(driver.title)

driver.switch_to.window(driver.window_handles[0])
driver.save_screenshot("playground_screenshot.png")

print(os.path.exists("playground_screenshot.png"))

print(driver.get_window_size())
driver.set_window_size(1280, 800)
print(driver.get_window_size())
driver.quit()

'''
Keeping the browser window at a consistent size ensures
that web elements appear in the same layout during every test.
This is especially important for responsive web applications,
where different window sizes may change the page layout.
'''