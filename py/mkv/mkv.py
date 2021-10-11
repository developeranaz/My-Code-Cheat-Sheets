from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')
driver.get("https://mkvking.me/injustice-2021/")
time.sleep(1)
driver.find_element_by_css_selector('#landing > div > center > img').click()
time.sleep(15)
driver.find_ > a').click()
time.sleep(15)

        driver = self.driver
        driver.get("https://mkvking.me/the-night-house-2020/")
        driver.find_element_by_link_text("GoogleDrive 720p").click()
        driver.get("https://tribuntekno.com/?id=SGdLN1RMS05YSUJwcDJSVlg0d09RdDd3YlYvSDV5RkdvWHBwZlBEcnpESVRCall1cmFvWmZQOStXTi9qY2FkbXRIcTZZZ21sSVNJRHkzU1BHa1lKM1YwYjE0YnEyN3NzVUdWaDJJa0tuMjA9")
        time.sleep(15)
        driver.find_element_by_xpath("//img[contains(@src,'https://tribuntekno.com/wp-content/uploads/button_im-not-a-robot.png')]").click()
        time.sleep(15)
        driver.find_element_by_xpath("//img[contains(@src,'https://tribuntekno.com/wp-content/uploads/button_generate-link.png')]").click()
        time.sleep(15)
        driver.find_element_by_id("showlink").click()

print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()

