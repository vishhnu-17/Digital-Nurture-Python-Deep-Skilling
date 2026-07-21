from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get("https://www.lambdatest.com/selenium-playground/")

# 36)

driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

driver.find_element(By.XPATH,
    "//button[contains(text(), 'Success Message')]"
).click()

success = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,".alert-success")))
assert "success message" in success.text

# 37) 

# Implicit Wait - time.sleep()
start = time.time()

driver.find_element(
    By.XPATH,
    "//button[contains(text(),'Success Message')]"
).click()

time.sleep(3)

alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")

print("Sleep Time:", time.time() - start)

driver.refresh()

# Explicit Wait - WebDriverWait()
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Success Message')]")
    )
)

start = time.time()

button.click()

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".alert-success")
    )
)

print("Explicit Wait Time:", time.time() - start)

'''
Comparison:

time.sleep(3):
- Execution Time: ~3.09 seconds
- Always waits for the full 3 seconds, even if the element is ready earlier.
- This makes the test slower and wastes time.

WebDriverWait (Explicit Wait):
- Execution Time: ~0.07 seconds
- Waits only until the required element becomes visible, then continues immediately.
- This makes the test much faster on fast machines.
- It is also more reliable on slow machines because it can wait up to the specified timeout instead of assuming the element will be ready after a fixed delay.

'''
# 38) 

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Success Message')]")
    )
)

button.click()

print("Button clicked successfully!")

'''
visibility_of_element_located():
Waits until the element is present and visible.

element_to_be_clickable():
Waits until the element is visible and enabled,
making it safe to click.
'''

# 39) 

driver.get("https://www.lambdatest.com/selenium-playground/")
driver.find_element(By.LINK_TEXT, "Table Data Search").click()

# Fluent Wait
wait = WebDriverWait(
    driver,
    timeout=10,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException]
)

row = wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "table tbody tr")
    )
)

print("First Row:")
print(row.text)

driver.quit()

