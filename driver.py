from selenium import webdriver
import requests
import os
import json
import time
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
    xpath_input = "//input[@name='q']"
    elem_input = driver.find_element_by_xpath(xpath_input)
    elem_input.send_keys('cheese')
    elem_input.submit()
    print(driver.title)
    
    #driver.save_screenshot("screenshot.png")
    #screenshot_base64 = driver.get_screenshot_as_base64()
    #print(screenshot_base64)
    driver.quit()

def login(link_login, cookie_url, pwd):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("w3c", False)
    chrome_options.add_argument("--user-data-dir=chrome-data")
    
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.implicitly_wait(10)
    
    driver.get(link_login)
    time.sleep(3)
    print(driver.title)
    
    # add cookie 
    myfile = requests.get(cookie_url)
    open('cookie.json', 'wb').write(myfile.content)
    with open('cookie.json', 'r') as f: 
        cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)
    print(os.listdir())

    driver.get(link_login)
    time.sleep(3)

    # input pwd
    xpath_password = "//input[@id='ap_password']"
    element_cell_input = driver.find_element_by_xpath(xpath_password)
    element_cell_input.clear()
    send_text = pwd
    element_cell_input.send_keys(send_text)
    time.sleep(1)

    xpath_login_button = "//input[@id='signInSubmit']"
    element_login_button = driver.find_element_by_xpath(xpath_login_button).click()
    time.sleep(5)
    screenshot_base64 = driver.get_screenshot_as_base64()
    print(screenshot_base64)
    print(driver.page_source)
    """    
    # check if login success, site loaded
    xpath_manage_orders = "//span[text()='Manage Orders']"

    try:
        driver.find_element_by_xpath(xpath_manage_orders)
        print('login success, site loaded')
    except:
        print('login problem')
        # if login problem, click fixup-phone-skip-link
        
        xpath_phone_skip = "//a[@id='ap-account-fixup-phone-skip-link']"

        try:
            element_phone_skip = driver.find_element_by_xpath(xpath_phone_skip)
            print('skip fixup phone')
            element_phone_skip.click()
            time.sleep(3)
        except Exception as e:
            print(e)
        else:
            pass
    """
    return driver

def check_message(driver, link_message):
    driver.get(link_message)
    time.sleep(5)
    
    xpath_threads = "//li[contains(@class, 'threads-list-thread')]/.."
    list_elem_threads = driver.find_elements_by_xpath(xpath_threads)
    list_links_threads = [element.get_attribute('href') for element in list_elem_threads]
    print(len(list_links_threads), 'messages')

    xpath_badge = "//li[contains(@class, 'threads-list-thread')]/div/kat-badge[@type='warning']/span[@class='warning']" # parent of parent node
    list_elem_badges = driver.find_elements_by_xpath(xpath_badge)

    list_expire = [int(re.search(r'\d+', element.text).group()) for element in list_elem_badges]
    
    dic_link_expire = dict(zip(list_links_threads, list_expire))
    expire_in_hours = 24 # in hours
    dic_link_under_limit = dict(filter(lambda item: item[1]<expire_in_hours, dic_link_expire.items()))
    list_link_under_limit = [k for k,v in dic_link_under_limit.items()]

    xpath_button_no_response_needed = "//kat-button[@label='No Response Needed']"
    
    if list_link_under_limit:
        for link_thread in list_link_under_limit:
            print(link_thread)
            driver.get(link_thread)
            button_no_response_needed = driver.find_element_by_xpath(xpath_button_no_response_needed)
            print(button_no_response_needed.get_attribute('label'))
            #button_no_response_needed.click()
    else:
        print('No messages')
        
    return driver

if __name__ == "__main__":
    driver_test()
    link_login = os.environ["LINK_LOGIN"]
    cookie_url = os.environ["COOKIE_URL"]
    pwd = os.environ["PWD"]
 #   driver = login(link_login, cookie_url, pwd)
    
 #   link_message = os.environ["LINK_MESSAGE"]
 #   driver = check_message(driver, link_message)
    
 #   driver.quit()
