from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.get("https://www.lambdatest.com/selenium-playground/")

driver.find_element(By.LINK_TEXT,"Simple Form Demo").click()

element = driver.find_element(By.ID,"user-message")
element = driver.find_element(By.NAME,"border border-gray-550 w-full h-35 rounded px-10")
element = driver.find_element(By.CLASS_NAME,"border")
element = driver.find_element(By.TAG_NAME,"input")

element = driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/main/div/section[2]/div/div/div/div[1]/div[2]/div/div[1]/input"
)
element = driver.find_element(
    By.XPATH,
    "//*[@id='user-message']"
)

driver.find_element(
    By.CSS_SELECTOR,
    "#user-message"
)

driver.find_element(
    By.CSS_SELECTOR,
    "input[type='text']"
)

driver.find_element(
    By.CSS_SELECTOR,
    "div > input"
)

driver.back()
driver.find_element(By.LINK_TEXT,"Checkbox Demo").click()

driver.find_element(
    By.XPATH,
    "//label[text()='Option 1']"
)

labels = driver.find_elements(
    By.XPATH,
    "//label[contains(text(),'Option')]"
)

print(len(labels))

for label in labels:
    print(label.text)


"""
Preferred Locator Ranking

1. ID
- Unique
- Fast
- Most stable

2. Name
- Usually unique
- Easy to read

3. CSS Selector
- Fast
- Flexible

4. Relative XPath
- Flexible
- Can locate by text or attributes

5. Class Name
- Often reused
- May not be unique

6. Absolute XPath
- Very fragile
- Breaks whenever HTML structure changes
"""