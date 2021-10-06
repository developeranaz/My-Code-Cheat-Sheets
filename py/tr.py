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
driver.find_element_by_id("mat-input-0").send_keys("peow568@mailto.plus")
time.sleep(1)
driver.find_element_by_id("mat-input-2").click()
driver.find_element_by_id("mat-input-2").click()
driver.find_element_by_id("mat-input-2").clear()
driver.find_element_by_id("mat-input-2").send_keys("Xhzoamxtqye1@")
driver.find_element_by_xpath("//form[@id='credential-form']/mat-form-field[4]/div/div/div[3]").click()
driver.find_element_by_id("mat-input-3").click()
driver.find_element_by_id("mat-input-3").clear()
driver.find_element_by_id("mat-input-3").send_keys("Xhzoamxtqye1@")
driver.find_element_by_xpath("//button[@id='continue-button']/span/span").click()

        # ERROR: Caught exception [ERROR:
time.sleep(2)

print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()
