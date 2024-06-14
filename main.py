import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import threading
import time

proxies = []
keys = ['ip','port','username','password']
with open('proxy.txt','r') as proxies_file:
    lines = proxies_file.readlines()
    for i in lines:
        proxies.append(dict(zip(keys,i.replace('\n','').split(':'))))
        
print(proxies)

def start_browser(proxy):
    # Start Adspower profile
    

    # Configure Selenium WebDriver with Adspower proxy
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy['ip']}:{proxy['port']}')

    # Start WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Use WebDriver as usual
    driver.get('https://whatismyipaddress.com/')

    # Perform desired actions here
    time.sleep(3)
    print(driver.find_element(By.ID,'ipv4').text())

    # Close the WebDriver
    driver.quit()

# List to keep track of threads
threads = []

# Create and start threads for each profile
for i in range(4):
    thread = threading.Thread(target=start_browser, args=(proxies[i],))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# print("All browsers have been started and closed.")
