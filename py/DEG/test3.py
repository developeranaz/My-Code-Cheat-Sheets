from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
options = Options()
#options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
#driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://degoo.com/")
time.sleep(2)
driver.find_element_by_css_selector('#accept-cookies').click()
time.sleep(2)
driver.find_element_by_css_selector('#Email').send_keys("kolpj875@mailto.plus")
driver.find_element_by_css_selector('#Password').send_keys("kolpj875@mailto.plus")
#avv = driver.page_source.encode("utf-8")
#os.system("echo $avv")
#print(avv)
#print(driver.page_source.encode("utf-8"))
driver.find_elements_by_class_name("button-turquoise button-fill").click()
#driver.find_element_by_css_selector('#mat-input-2').send_keys("Xhzoamxtqyei1@gmail.com")
#driver.find_element_by_css_selector('#mat-input-3').send_keys("Xhzoamxtqyei1@gmail.com")
#driver.find_element_by_css_selector('#continue-button').click()

#driver.quit()
