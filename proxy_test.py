import random
import copy
import os
import time
from selenium import webdriver

from selenium.webdriver.common.proxy import Proxy, ProxyType

#msg_list = []
#
#text = "Good luck"
#
#for i in range(10):
#	msg_list.append(text + str(i))
#	
#print(msg_list)

#backup = ['Good luck0', 'Good luck1', 'Good luck2', 'Good luck3', 'Good luck4', 'Good luck5', 'Good luck6', 'Good luck7', 'Good luck8', 'Good luck9']
#m = copy.deepcopy(backup)
#random.shuffle(m)
#print(backup)
#print(m)
#
#while(m):
#	print(m.pop())
#	
#print(m)
#
#if(not m):
#	m = copy.deepcopy(backup)
#	random.shuffle(m)
#	
#	
#print(m)


ip = "75.121.81.97"
port = "58093"
PROXY = "184.0.77.60:13529"

## Create a copy of desired capabilities object.
#desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
## Change the proxy properties of that copy.
#desired_capabilities['proxy'] = {
#	"httpProxy":PROXY,
#	"ftpProxy":PROXY,
#	"sslProxy":PROXY,
#	"noProxy":None,
#	"proxyType":"MANUAL",
#	"class":"org.openqa.selenium.Proxy",
#	"autodetect":False
#}

# you have to use remote, otherwise you'll have to code it yourself in python to 
# dynamically changing the system proxy preferences
#driver = webdriver.Remote("http://whatismyipaddress.com", desired_capabilities=desired_capabilities)
#DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
#driver = webdriver.Chrome(DRIVER_PATH, desired_capabilities=desired_capabilities)
#driver.get("http://whatismyipaddress.com")

#DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
#driver = webdriver.Chrome(DRIVER_PATH)
#proxy = webdriver.Proxy()
#proxy.proxy_type=ProxyType.MANUAL
#proxy.http_proxy= PROXY  
#proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
#driver.start_session(webdriver.DesiredCapabilities.CHROME)
#driver.get("http://whatismyipaddress.com")

prox = Proxy()
prox.proxy_type = ProxyType.MANUAL
prox.http_proxy = PROXY
prox.socks_proxy = PROXY
prox.ssl_proxy = PROXY

capabilities = webdriver.DesiredCapabilities.CHROME
prox.add_to_capabilities(capabilities)

DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
driver = webdriver.Chrome(DRIVER_PATH,desired_capabilities=capabilities)
driver.get("http://whatismyipaddress.com")

#DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver")
#options = webdriver.ChromeOptions()
#options.add_argument('--proxy-server=http://184.0.77.60:13529')
#driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)
#driver.get("http://whatismyipaddress.com")

time.sleep(20)
