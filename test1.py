from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import json
import os

# Path to FoxyProxy extension (you need to download it)
foxyproxy_extension_path = 'foxyproxy_standard-8.9.xpi'
foxyproxy_auto_config_path = 'foxyproxy_auto_config.zip'

# Proxy details
proxy_host = "38.154.227.167"
proxy_port = "5868"
proxy_username = "ihzrgsvj"
proxy_password = "2pbv1q3sw645"

# Create a new Firefox profile
profile = webdriver.FirefoxProfile()


# Configure Firefox options
options = Options()
options.profile = profile

# Path to the geckodriver executable
driver_path = 'geckodriver.exe'

# Initialize WebDriver with the profile and options
driver = webdriver.Firefox(service=Service(driver_path), options=options)

driver.install_addon(foxyproxy_extension_path, temporary=True)
driver.install_addon(foxyproxy_auto_config_path, temporary=True)

# Inject proxy settings via JavaScript
proxy_settings = {
    'host': proxy_host,
    'port': proxy_port,
    'username': proxy_username,
    'password': proxy_password
}

script = f"""
browser.storage.local.set({{
    proxySettings: {proxy_settings}
}});
"""

# Inject the script to configure the proxy
driver.execute_script(script)

# Open a URL to test the proxy
driver.get("https://whatismyipaddress.com/")

# Perform your browser automation tasks
# ...

# Close the browser
driver.quit()
