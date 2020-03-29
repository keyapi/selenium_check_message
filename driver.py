from selenium import webdriver
import requests
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def driver_test():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("w3c", False)

    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.implicitly_wait(10)

    # driver version
    if 'browserVersion' in driver.capabilities:
        driver_version = driver.capabilities['browserVersion']
    else:
        driver_version = driver.capabilities['version']

    if driver_version[:9] == '80.0.3987':
        print(f"good, driver_version is {driver_version}")
    else:
        print(f"! driver_version is {driver_version}, not 80.0.3987")

    link = "https://www.google.com"

    driver.get(link)
    xpath_google_img = "//img[@alt='Google']"
    elem_google_img = driver.find_element_by_xpath(xpath_google_img)
    print(elem_google_img.get_attribute('src')
    driver.quit()

if __name__ == "__main__":
    driver_test()
