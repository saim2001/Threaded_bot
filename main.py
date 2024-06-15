import requests
import threading
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options


proxies = []
keys = ['ip','port','username','password']
with open('proxy.txt','r') as proxies_file:
    lines = proxies_file.readlines()
    for i in lines:
        proxies.append(dict(zip(keys,i.replace('\n','').split(':'))))
        
print(proxies)


# Function to get a random user agent
def get_random_user_agent():
    ua = UserAgent()
    print(ua.random)
    return ua.random


def start_browser(proxy):

   
    
    options = Options()
    options.set_preference("general.useragent.override", get_random_user_agent())

    ## Define Your Proxy Endpoint
    # Start WebDriver
    driver = webdriver.Firefox(service=Service('geckodriver.exe') ,options=options)

    time.sleep(2)

    # alert = webdriver.switch_to.alert()
    # print("switched to alert window")
    # alert.send_keys(proxy['username'] + Keys.TAB + proxy['password'])
    # alert.accept()
    # webdriver.switch_to.default_content()

    # Use WebDriver as usual
    print(driver.execute_script("return navigator.userAgent;"))
    driver.get('https://www.youtube.com/watch?v=rAm5FOo_oD8')

    
    # Perform desired actions here
    time.sleep(3)
    print(driver.find_element(By.ID,'ipv4').text)

    # Close the WebDriver
    driver.quit()

# List to keep track of threads
threads = []


start_browser(proxies[-1])

# Create and start threads for each profile
# for i in range(4):
#     thread = threading.Thread(target=start_browser, args=(proxies[i],))
#     threads.append(thread)
#     thread.start()

# Wait for all threads to complete
# for thread in threads:
#     thread.join()

# print("All browsers have been started and closed.")
