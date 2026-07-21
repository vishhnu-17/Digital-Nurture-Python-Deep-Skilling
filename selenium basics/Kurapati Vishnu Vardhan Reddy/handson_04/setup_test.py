"""
Selenium Components

1. WebDriver
- WebDriver is the main Selenium component used to automate web browsers.
- It communicates with the browser using browser-specific drivers such as ChromeDriver.
- It sends commands like click(), send_keys(), get(), etc., to the browser.

2. Selenium Grid
- Selenium Grid allows tests to run on multiple machines, browsers, and operating systems simultaneously.
- It is mainly used for parallel execution to reduce testing time.

3. Selenium IDE
- Selenium IDE is a browser extension that records and plays back user actions.
- It can also generate Selenium code in different programming languages.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

'''
Implicit wait tells Selenium to wait up to 10 seconds when locating elements.
It is generally not recommended because it applies globally to all element searches.
Explicit waits are preferred since they wait only for specific conditions,
making tests faster and more reliable.
'''

driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

print(driver.title)
driver.quit()