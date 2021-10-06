from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://app.treasure.cloud/auth/signup?code=YzNkNGVmZDUtMjZiOS0xMWVjLWFmNzgtMWY5NWYyY2E3NDhhOmYwYTE0NjdhLTMyYzEtMTFlYi1iMWI4LTViYTQzMmY1ZjBkMA%3D%3D")
time.sleep(10)
driver.find_element_by_id("mat-input-0").click()
driver.find_element_by_id("mat-input-0").clear()
driver.find_element_by_id("mat-input-0").send_keys("xxxxmail")
time.sleep(1)
driver.find_element_by_id("mat-input-1").click()
driver.find_element_by_id("mat-input-1").click()
driver.find_element_by_id("mat-input-1").clear()
driver.find_element_by_id("mat-input-1").send_keys("xxxxstrongpass")
time.sleep(2)
print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()
