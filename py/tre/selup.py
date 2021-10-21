from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import pyautogui
options = Options()
options.headless = True
#driver = webdriver.Firefox(options=options, executable_path=r'E:\Downloads\geckodriver.exe')
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://app.treasure.cloud/auth/signin")

driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(3)').click()
time.sleep(2)
driver.find_element_by_css_selector('#mat-input-0').send_keys("dhamu@mailsac.com")
driver.find_element_by_css_selector('#mat-input-1').send_keys("AnaZ1234#")

driver.find_element_by_css_selector('#signin-button').click()
time.sleep(10)
driver.find_element_by_css_selector('button.mat-menu-trigger:nth-child(1)').click()
time.sleep(3)
driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(2)').click()
time.sleep(2)
#driver.find_element_by_css_selector('button.mat-focus-indicator:nth-child(2) > div:nth-child(1) > div:nth-child(2)').send_keys("/home/dev/1.zip")
pyautogui.write('/home/dev/2.zip')
time.sleep(2)
pyautogui.press('enter')

