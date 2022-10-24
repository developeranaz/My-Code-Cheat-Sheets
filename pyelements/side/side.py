from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
options = Options()
#options.headless = True


driver = webdriver.Firefox(options=options, executable_path=r'/usr/bin/geckodriver')

path = r"/selenium_ide_firefox-3.17.4.xpi"
driver.install_addon(path, temporary=True)

driver.profile = webdriver.FirefoxProfile()
driver.profile.add_extension(path)
driver.profile.set_preference("security.fileuri.strict_origin_policy", False)
driver.get("about:debugging#/runtime/this-firefox")
time.sleep(2)

print(driver.page_source.encode("utf-8"))
print ("Headless Firefox Initialized")
driver.quit()
