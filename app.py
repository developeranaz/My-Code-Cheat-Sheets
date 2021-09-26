from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
#chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)
start_url = "https://booyah.live/channels/34884818"
driver.get(start_url)
time.sleep(12000)
print(driver.page_source.encode("utf-8"))
driver.quit()
# b'<!DOCTYPE html><
