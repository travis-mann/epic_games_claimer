#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""epic_driver.py: extend chrome_ for epic games site specific actions"""

__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from chrome_driver import ChromeDriver

import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# --- classes ---
class EpicDriver(ChromeDriver):
    """
    purpose: extend chrome_ for epic games site specific actions
    """
    def __init__(self):
        # init parent class
        super(EpicDriver, self).__init__()
        
        # instance attributes
        self.logged_in_url = "https://store.epicgames.com"
        
        # track states
        self.logged_in = False

    def handle_captcha(self):
        """
        purpose: search for and attempt to complete captcha
        """
        print('searching for captcha...')
        # shorten timeout
        original_timeout = self.timeout
        self.timeout = 10

        # search for captcha
        try:
            self.find(By.XPATH, "//*[text()='Please complete a security check to continue']")
        except:
            print('no captcha detected!')
        else:
            input('please solve captcha and press enter...')
            # raise ValueError('captcha detected!')

        # reset timeout
        self.timeout = original_timeout

    def login(self) -> None:
        """
        purpose: go to epic games and login. Use credentials configured in environment variables
        """
        # go to epic games page
        print(f'going to {self.logged_in_url}...')
        self.get(self.logged_in_url)

        # check for captcha
        self.handle_captcha()

        # check if already logged in
        username = os.environ['USERNAME']
        try:
            self.find_element(By.XPATH, f"//*[text()='{username}']")
            print('skipping login, already logged in!')
            self.logged_in = True
            return
        except:
            print('logging in...')

        # check for captcha
        self.handle_captcha()

        # click login button
        login_button = self.find(By.XPATH, '//*[@id="user"]/ul/li/a/span', clickable=True)
        login_button.click()

        # select "Sign in with Epic Games"
        sign_in_with_epic_games_button = self.find(By.ID, "login-with-epic", clickable=True)
        sign_in_with_epic_games_button.click()

        # input credentials from environment variables
        email_text_box = self.find(By.ID, "email")
        email_text_box.send_keys(os.environ["EMAIL"])

        password_text_box = self.find(By.ID, "password")
        password_text_box.send_keys(os.environ["PASSWORD"])

        # submit credentials
        password_text_box.send_keys(Keys.ENTER)

        # handle possible captcha
        self.handle_captcha()

        # validate successful login
        try:
            login_validation_element = self.find(By.XPATH, '//*[@id="SearchLayout"]/div[2]/div/input')
        except Exception as e:
            print(f'login FAILED! Current URL: {self.current_url}')
            raise e
        else:
            print('login success!')
            self.logged_in = True

    def claim(self) -> None:
        """
        purpose: navigate to claim current free game once logged in
        """
        if not self.logged_in:
            self.login()
        
        # find free element
        print('clicking on free game...')
        free_now_button = self.find(By.XPATH, "//*[text()='Free Now']", clickable=True)
        free_now_button.click()

        # click get
        print('clicking "Get"...')
        get_button = self.find(By.XPATH,
                               '//*[@id="dieselReactWrapper"]/div/div[4]/main/div[2]/div/div/div/div[2]/div[4]/div/aside/div/div/div[6]/div/button',
                               clickable=True)
        get_button.click()

        # validate price is $0.00
        print('checking price...')
        try:
            total_container = self.find(By.XPATH, '//*[@id="payment-summaries__scroll-container"]/div[2]/div[3]')
            total_container.find_element(By.XPATH, "//*[text()='$0.00']")
        except Exception as e:
            print('Loaded item is not free! Aborting!')
            raise e

        # click place order
        print('clicking "Place Order"...')
        place_order_button = self.find(By.XPATH, '//*[@id="purchase-app"]/div/div/div/div[2]/div[2]/div/button/div/div',
                                       clickable=True)
        place_order_button.click()