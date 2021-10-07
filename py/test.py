from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
driver.get("https://app.treasure.cloud/auth/signup?code=YzNkNGVmZDUtMjZiOS0xMWVjLWFmNzgtMWY5NWYyY2E3NDhhOmYwYTE0NjdhLTMyYzEtMTFlYi1iMWI4LTViYTQzMmY1ZjBkMA==")
time.sleep(10)
driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(3)').click()
time.sleep(2)
driver.find_element_by_css_selector('#mat-input-0').send_keys("jan888012@mailto.plus")
driver.find_element_by_css_selector('#mat-input-1').send_keys("jan888012@mailto.plus")
driver.find_element_by_css_selector('#mat-input-2').send_keys("Xhzoamxtqyei1@gmail.com")
driver.find_element_by_css_selector('#mat-input-3').send_keys("Xhzoamxtqyei1@gmail.com")
driver.find_element_by_css_selector('#continue-button').click()
#verify-code-form > div:nth-child(1) > div:nth-child(1) > input:nth-child(1) 
#verify-code-form > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').send_keys("1")
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)').send_keys("1")
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(3) > input:nth-child(1)').send_keys("1")
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(4) > input:nth-child(1)').send_keys("1")
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(5) > input:nth-child(1)').send_keys("1")
driver.find_element_by_css_selector('#verify-code-form > div:nth-child(1) > div:nth-child(6) > input:nth-child(1)').send_keys("1")
##mat-input-0 #mat-input-0 #continue-button
print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
#driver.quit()   #mat-input-1   #signin-button 
#accept  
#mat-checkbox-1 > label:nth-child(1) > div:nth-child(1)   
#mat-checkbox-2 > label:nth-child(1) > div:nth-child(1)

.primary-action  or /html/body/div[2]/div[2]/div/mat-dialog-container/app-preferences-dialog/div/div[3]/button

#20gigs
.primary-action
.primary-action > span:nth-child(1)
.primary-action

