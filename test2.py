import ctypes
import traceback
from dataclasses import asdict
import threading
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import itertools
from browserforge.fingerprints import FingerprintGenerator, Screen
import utils
import time

# Proxy details
proxies = []
keys = ['ip', 'port', 'username', 'password']
with open('proxy.txt', 'r') as proxies_file:
    lines = proxies_file.readlines()
    for i in lines:
        proxies.append(dict(zip(keys, i.replace('\n', '').split(':'))))


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


def scroll_and_zoomout(driver):
    utils.scroll_to_half(driver)
    utils.scroll_to_bottom(driver)
    utils.scroll_to_top(driver)
    utils.zoomout(driver)


def iframe_handling(driver, iframes, tabs):
    for iframe in iframes:
        # driver.execute_script("arguments[0].scrollIntoView();", iframe)

        # driver.execute_script("arguments[0].click();", iframe)
        driver.switch_to.frame(iframe)
        # Execute JavaScript to click the element inside the iframe
        # script = """
        # let ads = document.querySelectorAll('your-ad-selector'); // Change 'your-ad-selector' to the actual selector for ads
        # ads.forEach(ad => {
        #     let newTab = window.open(ad.href, '_blank');
        #     newTab.focus();
        # });
        # """

        try:

            src = utils.wait_for_element_to_load(
                By.XPATH, '//a[@target="_top"]', driver)
            if src:
                print('-----Ad Found-----')
                src.send_keys(Keys.CONTROL + Keys.RETURN)
                # driver.execute_script(
                #     "window.open(arguments[0].getAttribute('href'));", src)
                # driver.execute_script(
                #     "window.open(arguments[0].href, '_blank');", src)
                driver.switch_to.default_content()
                driver.switch_to.window(driver.window_handles[tabs])
                scroll_and_zoomout(driver)
                driver.close()
                driver.switch_to.window(driver.window_handles[tabs-1])
                break

        except Exception as e:
            traceback.print_exc()
            print('-----Ad Not Found-----')
            pass

        driver.switch_to.default_content()


def start_automation(driver):

    driver.get('https://www.youtube.com/@brandtech9253/community')
    try:
        utils.wait_for_element_to_load(
            By.XPATH, "(//button[@aria-label='Accept all'])[1]", driver, 8).click()
    except:
        pass

    link = utils.wait_for_element_to_load(
        By.XPATH, "//*[@id='contentTextExpander']//a", driver)
    driver.get(link.get_attribute('href'))
    time.sleep(3)
    scroll_and_zoomout(driver)
    iframes = utils.wait_for_elements_to_load(By.XPATH, '//iframe', driver)
    iframe_handling(driver, iframes, 1)
    links = utils.wait_for_elements_to_load(
        By.XPATH, "//*[contains(@class,'link')]", driver)
    for i in range(4):
        # Simulate opening the link in a new tab (Ctrl/Command + click)
        links[i].send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        scroll_and_zoomout(driver)
        iframes_posts = utils.wait_for_elements_to_load(
            By.XPATH, '//iframe', driver)
        iframe_handling(driver, iframes_posts, 2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def start_browser(proxy):
    # Create proxy options
    proxy_options = {
        'proxy': {
            'http': f'http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}',
            'https': f'https://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}',
            'no_proxy': 'localhost,127.0.0.1'  # Bypass the proxy for localhost
        }
    }
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    screen = Screen(
        min_width=screen_width,
        max_width=screen_width,
        min_height=screen_height,
        max_height=screen_height
    )

    # Example fingerprint data (replace with your actual fingerprint data)
    fingerprints = FingerprintGenerator()
    fingerprint = fingerprints.generate(screen=screen)
    print(
        f'-----Generated FingerPrint-------\n{fingerprint.navigator.userAgent}')
    # Set up Firefox options
    firefox_options = webdriver.FirefoxOptions()
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile = apply_fingerprint_to_profile(
        asdict(fingerprint), firefox_profile)
    firefox_options.profile = firefox_profile
    # Initialize the WebDriver with Selenium Wire
    driver = webdriver.Firefox(seleniumwire_options=proxy_options,
                               options=firefox_options)

    user_agent = driver.execute_script("return navigator.userAgent;")
    print(f'-----FingerPrint Used-------\n{user_agent}')

    # Open a URL to test the proxy
    driver.get('https://httpbin.org/ip')
    ip_element = utils.wait_for_element_to_load(
        By.XPATH, "//span[contains(@class,'objectBox')]", driver)
    ip_address = ip_element.text
    print(f'-----Ip address used-------\n{ip_address}')
    start_automation(driver)


proxy_iter = iter(proxies)
threads = []

start_browser(proxies[0])

# while True
#     chunk = list(itertools.islice(proxy_iter, 4))
#     if not chunk:
#         break
#     for i in range(len(chunk)):
#         thread = threading.Thread(target=start_browser, args=(chunk[i],))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

# Perform your browser automation tasks
# ...

# Close the browser
# driver.quit()
