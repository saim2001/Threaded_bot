import ctypes
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from browserforge.fingerprints import FingerprintGenerator, Screen
from selenium.webdriver.common.proxy import Proxy, ProxyType
import pprint
import json
from dataclasses import asdict

proxies = []
keys = ['ip', 'port', 'username', 'password']
with open('proxy.txt', 'r') as proxies_file:
    lines = proxies_file.readlines()
    for i in lines:
        proxies.append(dict(zip(keys, i.replace('\n', '').split(':'))))

print(proxies)


def configure_proxy(proxy, profile):
    proxy_host = proxy['ip']
    proxy_port = proxy['port']

    # Set up the proxy configuration
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = f"{proxy_host}:{proxy_port}"
    proxy.ssl_proxy = f"{proxy_host}:{proxy_port}"

    # Configure the proxy settings
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy_host)
    profile.set_preference("network.proxy.http_port", int(proxy_port))
    profile.set_preference("network.proxy.ssl", proxy_host)
    profile.set_preference("network.proxy.ssl_port", int(proxy_port))

    # Optionally disable the proxy for localhost
    firefox_profile.set_preference(
        "network.proxy.no_proxies_on", "localhost, 127.0.0.1")


# Function to handle proxy authentication


def set_proxy_authentication(driver, proxy_username, proxy_password):
    driver.get("about:config")
    driver.execute_script(f"""
        Components.classes['@mozilla.org/preferences-service;1']
            .getService(Components.interfaces.nsIPrefBranch)
            .setCharPref('network.proxy.login', '{proxy_username}');
        Components.classes['@mozilla.org/preferences-service;1']
            .getService(Components.interfaces.nsIPrefBranch)
            .setCharPref('network.proxy.password', '{proxy_password}');
    """)


def apply_fingerprint_to_profile(fingerprint, profile):
    for category, properties in fingerprint.items():
        if category == 'screen':
            for key, value in properties.items():
                if key == 'devicePixelRatio':
                    profile.set_preference(
                        "layout.css.devPixelsPerPx", str(value))
                    profile.set_preference(
                        "devtools.toolbox.zoomValue", str(value))
        elif category == 'navigator':
            for key, value in properties.items():
                if key == 'userAgent':
                    profile.set_preference("general.useragent.override", value)
                elif key == 'language':
                    profile.set_preference("intl.accept_languages", value)
                elif key == 'platform':
                    profile.set_preference("dom.navigator.platform", value)
                elif key == 'hardwareConcurrency':
                    profile.set_preference("dom.maxHardwareConcurrency", value)
                elif key == 'extraProperties':
                    for prop, prop_value in value.items():
                        if prop == 'pdfViewerEnabled':
                            profile.set_preference(
                                "pdfjs.disabled", not prop_value)
                        elif prop == 'isBluetoothSupported':
                            profile.set_preference(
                                "dom.bluetooth.enabled", prop_value)
                        elif prop == 'vendorFlavors':
                            for i, flavor in enumerate(prop_value):
                                profile.set_preference(
                                    f"general.appname.override_{i}", flavor)
        elif category == 'headers':
            for header, header_value in properties.items():
                if header == 'User-Agent':
                    profile.set_preference(
                        "general.useragent.override", header_value)
                elif header == 'Accept-Language':
                    profile.set_preference(
                        "intl.accept_languages", header_value)
                # Add more headers as needed
        # Add more categories as needed

    return profile


user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

screen = Screen(
    min_width=screen_width-100,
    max_width=screen_width,
    min_height=screen_height-100,
    max_height=screen_height
)

# Example fingerprint data (replace with your actual fingerprint data)
fingerprints = FingerprintGenerator(screen=screen)


# Configure Firefox options
firefox_options = Options()
firefox_profile = webdriver.FirefoxProfile()

# Apply the fingerprint to the Firefox profile
firefox_profile = apply_fingerprint_to_profile(
    asdict(fingerprints.generate(os='windows')), firefox_profile)

configure_proxy(proxies[0], firefox_profile)


# Apply the profile to options
firefox_options.profile = firefox_profile

# Initialize WebDriver
# Replace with the actual path to geckodriver
driver_path = 'geckodriver.exe'
driver = webdriver.Firefox(
    service=Service('geckodriver.exe'), options=firefox_options)
print(driver.execute_script("return navigator.userAgent;"))
set_proxy_authentication(
    driver, proxies[0]['username'], proxies[0]['password'])
# Open a URL
driver.get("https://whatismyipaddress.com/")

# Perform your browser automation tasks
# ...

# Close the browser
# driver.quit()
