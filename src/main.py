#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main.py: high level selenium navigation logic"""

__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
import chromedriver_autoinstaller
import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# --- funcs ---
# ADD FIND FUNCTION WITH WAITS FOR FINDING ELEMENTS

def init_driver(headless: bool = False) -> webdriver:
    """
    purpose: create a chrome webdriver with required chrome settings
    :param headless: launches invisible browser if true
    :return driver: chrome webdriver
    """

    # automatically grab correct chrome driver for current chrome browser version
    chromedriver_autoinstaller.install()

    # configure chrome options
    options = webdriver.ChromeOptions()

    # specify specific location for profile data
    options.add_argument(fr"--user-data-dir={os.getcwd()}\profile_data")

    # add headless argument if specified
    if headless:
        options.add_argument("--headless=new")
    else:  # maximize window
        options.add_argument("--start-maximized")

    # create driver with configured options
    return webdriver.Chrome(options=options)


def login(driver: webdriver) -> None:
    """
    purpose: go to epic games and login. Use credentials configured in environment variables
    """
    # go to epic games page
    driver.get("https://store.epicgames.com")

    # click login button
    login_button = driver.find_element(By.XPATH, '//*[@id="user"]/ul/li/a/span')
    login_button.click()

    # select "Sign in with Epic Games"
    sign_in_with_epic_games_button = driver.find_element(By.ID, "login-with-epic")
    sign_in_with_epic_games_button.click()

    # input credentials from environment variables
    email_text_box = driver.find_element(By.ID, "email")
    email_text_box.send_keys(os.environ["USERNAME"])

    password_text_box = driver.find_element(By.ID, "password")
    password_text_box.send_keys(os.environ["PASSWORD"])

    # submit credentials
    password_text_box.send_keys(Keys.ENTER)

    # check for captcha
    print('searching for captcha...')
    try:
        captcha_element = driver.find_element(By.XPATH, "//*[text()='Please complete a security check to continue']")
    except:
        print('no captcha detected!')
    else:
        print('captcha detected!')
        # raise ValueError('CAPTCHA DETECTED!')
        input("please complete captcha to continue.")

    # validate successful login
    try:
        login_validation_element = driver.find_element(By.XPATH, '//*[@id="SearchLayout"]/div[2]/div/input')
    except Exception as e:
        print('login FAILED!')
        raise e
    else:
        print('login success!')


# --- main ---
if __name__ == "__main__":
    # initialize driver
    driver = init_driver()

    # login
    login(driver)

    # find free element
    free_now_button = driver.find_element(By.XPATH, "//*[text()='Free Now']")
    free_now_button.click()

    # click get
    get_button = driver.find_element(By.XPATH, '//*[@id="dieselReactWrapper"]/div/div[4]/main/div[2]/div/div/div/div[2]/div[4]/div/aside/div/div/div[6]/div/button')
    get_button.click()

    # validate price is $0.00
    try:
        driver.find_element(By.XPATH, '//*[@id="payment-summaries__scroll-container"]/div[2]/div[3]/*[@innertext="$0.00"]')
    except Exception as e:
        print('Loaded item is not free! Aborting!')
        raise e

    # click place order
    place_order_button = driver.find_element(By.XPATH, '//*[@id="purchase-app"]/div/div/div/div[2]/div[2]/div/button/div/div')
    place_order_button.click()

    # pause for user validation
    input("validate free item redeemed (click enter to continue)...")

    # clean up resources
    driver.close()
