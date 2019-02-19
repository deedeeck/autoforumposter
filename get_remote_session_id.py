import time
from selenium import webdriver


DRIVER_PATH = ("/Users/yh/Desktop/chromedriver")
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument("user-agent=" + USER_AGENT)


url = "http://127.0.0.1:4444/wd/hub"
driver = webdriver.Remote(command_executor=url, desired_capabilities=options.to_capabilities())

session_id = ""

if session_id :
	driver.session_id = session_id
else :
	print(driver.session_id)
	driver.get('https://www.bbc.com/')

driver.get('https://www.yahoo.com.my')