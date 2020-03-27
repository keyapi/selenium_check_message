import requests
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)

chrome_options.add_experimental_option("w3c", False)

driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver.implicitly_wait(5)

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

driver.quit()

if __name__ == "__main__":
    main()
