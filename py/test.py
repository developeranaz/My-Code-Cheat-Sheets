from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
driver.get("https://app.treasure.cloud/auth/signup?code=YzNkNGVmZDUtMjZiOS0xMWVjLWFmNzgtMWY5NWYyY2E3NDhhOmYwYTE0NjdhLTMyYzEtMTFlYi1iMWI4LTViYTQzMmY1ZjBkMA==")
time.sleep(10)
driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(3)').click()
driver.find_element_by_css_selector('mat-form-field.mat-form-field:nth-child(2) > div:nth-child(1) > div:nth-child(1)').click()

print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
#driver.quit()
