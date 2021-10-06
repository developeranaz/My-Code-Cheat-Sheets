from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://app.treasure.cloud/auth/signup?code=YzNkNGVmZDUtMjZiOS0xMWVjLWFmNzgtMWY5NWYyY2E3NDhhOmYwYTE0NjdhLTMyYzEtMTFlYi1iMWI4LTViYTQzMmY1ZjBkMA%3D%3D")
time.sleep(15)
driver.find_element_by_id("mat-button-wrapper").click()
time.sleep(3)
driver.find_element_by_id("mat-input-0").send_keys("peow568@mailto.plus")
time.sleep(1)
driver.find_element_by_id("mat-input-2").send_keys("Xhzoamxtqye1@")
time.sleep(1)
driver.find_element_by_id("mat-input-3").send_keys("Xhzoamxtqye1@")
time.sleep(1)
#driver.find_element_by_xpath("//body[@id='tm-body']/main/div/div/div[2]/div[2]/div/div/div/div[4]/ul/li[3]/div/a/span[2]").click()
driver.find_element_by_id("continue-button").click()
#document.getElementsByClassName('')[4
        # ERROR: Caught exception [ERROR:
time.sleep(2)

print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()
