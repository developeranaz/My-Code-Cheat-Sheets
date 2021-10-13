from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
options = Options()
options.headless = True
#driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
theinviteurl = open('/theinviteurl', 'r').read()
driver.get(theinviteurl)
time.sleep(2)
driver.find_element_by_css_selector('#accept-cookies').click()
time.sleep(2)
thechangingmail = open('/thechangingmail', 'r').read()
driver.find_element_by_css_selector('#Email').send_keys("kolpj875@mailto.plus")
driver.find_element_by_css_selector('#Password').send_keys("kolpj875@mailto.plus")
fullhtmlfile = driver.page_source.encode("utf-8")
print(fullhtmlfile, file=open("/output.html", "a"))
os.system("degoobtnfinder")
thechangingbtn = open('/thenewbtn', 'r').read()
print(thechangingbtn)
driver.find_element_by_css_selector(thechangingbtn).click()
time.sleep(5)
driver.find_element_by_css_selector(".product-free > div:nth-child(12) > div:nth-child(1) > a:nth-child(1)").click()
time.sleep(5)

