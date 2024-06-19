from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from selenium.webdriver.common.keys import Keys
import random

import warnings

#  utils - functions

# create connection


def waitforelemtobeclickable(by, selector, driver, t=25):
    element_clickable = EC.element_to_be_clickable((by, selector))
    element = WebDriverWait(driver, t).until(element_clickable)

    return element


def waitandclickelem(locator, selector, driver, t=15):
    if locator == "XPATH":
        element_present = EC.presence_of_element_located((By.XPATH, selector))
        element = WebDriverWait(driver, t).until(element_present)
    elif locator == "CSS":
        element_present = EC.presence_of_element_located(
            (By.CSS_SELECTOR, selector))
        element = WebDriverWait(driver, t).until(element_present)
    else:
        element_present = EC.presence_of_element_located((By.ID, selector))
        element = WebDriverWait(driver, t).until(element_present)

    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)


def wait_and_click(by, selector, driver, t=10):
    element_present = EC.presence_of_element_located((by, selector))
    element = WebDriverWait(driver, t).until(element_present)

    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)


def checkifelemexists(css, driver):
    try:
        # return driver.find_element_by_xpath(xpath)
        return driver.find_element(By.CSS_SELECTOR, css)
    except:
        return None


def wait_for_element_to_load(by, selector, driver, t=25):
    element_present = EC.presence_of_element_located((by, selector))
    element = WebDriverWait(driver, t).until(element_present)

    return element


def wait_for_elements_to_load(by, selector, driver, t=25):
    element_present = EC.presence_of_all_elements_located((by, selector))
    element_lst = WebDriverWait(driver, t).until(element_present)
    return element_lst


def scroll_to_half(driver):
    driver.execute_script(
        "window.scrollTo({top : Math.ceil(document.body.scrollHeight/2), behavior : 'smooth'});"
    )
    time.sleep(3)

    # driver.execute_script(
    # "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
    # )


def scroll_to_top(driver):
    driver.execute_script(
        "window.scrollTo({top:-document.body.scrollHeight,behavior:'smooth'});"
    )
    time.sleep(3)
    # driver.execute_script(
    #     "window.scrollTo(0, 0);"
    # )


def scroll_to_bottom(driver):
    driver.execute_script(
        "window.scrollTo({top:document.body.scrollHeight,behavior:'smooth'});"
    )
    time.sleep(4)

    # driver.execute_script(
    #     "window.scrollTo(0, document.body.scrollHeight);"
    # )


def page_not_found(driver):
    """ function to manage 404 page """
    for _ in range(3):
        if "Page not found" in driver.page_source:
            driver.refresh()
            time.sleep(3)
        else:
            break


def teardown(driver):
    # driver.close()
    driver.quit()
    print("Driver successfully closed")


def zoomout(driver):
    driver.execute_script("document.body.style.zoom='75%'")
    return 0
