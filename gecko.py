from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://google.com")
time.sleep(10)
print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()
