from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
#driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://app.treasure.cloud/auth/signup?code=Zjk4NDZkYWUtYzYyNC0xMWViLWJkY2QtMWQ4ZGMxNjU2NzdiOmYwYTE0NjdhLTMyYzEtMTFlYi1iMWI4LTViYTQzMmY1ZjBkMA==")
time.sleep(10)
driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(3)').click()
time.sleep(2)
driver.find_element_by_css_selector('#mat-input-0').send_keys("therandommail")
driver.find_element_by_css_selector('#mat-input-1').send_keys("therandommail")
driver.find_element_by_css_selector('#mat-input-2').send_keys("Xhzoamxtqyei1@gmail.com")
driver.find_element_by_css_selector('#mat-input-3').send_keys("Xhzoamxtqyei1@gmail.com")
driver.find_element_by_css_selector('#continue-button').click()
driver.quit()
