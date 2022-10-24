from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os

options = Options()
# options.headless = True


driver = webdriver.Firefox(options=options, executable_path=r"/usr/bin/geckodriver")

path = r"/selenium_ide_firefox-3.17.4.xpi"
driver.install_addon(path, temporary=True)

driver.profile = webdriver.FirefoxProfile()
driver.profile.add_extension(path)
driver.profile.set_preference("security.fileuri.strict_origin_policy", False)
driver.get("about:debugging#/runtime/this-firefox")
time.sleep(2)

# getting ex id
# print(driver.page_source.encode("utf-8"))
print("Getting Unique Id Link")
os.system("bash clear.sh")
with open("gen.html", "w") as f:
    f.write(driver.page_source)

os.system("bash getEXid.sh")
exid = open("geninput", "r").read()
print(exid)

driver.get(exid)

time.sleep(1)
os.system("bash clear.sh")
time.sleep(5)
with open("gen.html", "w") as f:
    f.write(driver.page_source)
os.system("bash gen.sh")

time.sleep(3)
variable = open("geninput", "r").read()
print(variable)
time.sleep(3)
driver.find_element_by_css_selector(variable).send_keys(os.getcwd() + "/4.side")

time.sleep(3)

driver.find_element_by_css_selector(".si-play-all").click()


driver.quit()
