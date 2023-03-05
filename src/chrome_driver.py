#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""chrome_driver.py: Chrome Webdriver extension to implement better waits"""

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
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# --- classes ---
class ChromeDriver(webdriver.Chrome):
    """
    purpose: Chrome Webdriver extension to implement better waits
    """
    def __init__(self, headless: bool = False, timeout: int = 30):
        """
        :param headless: launches invisible browser if true, else visible browser
        :param timeout: time to resolve expected conditions before throwing exceptions during actions
        """
        # store instance attributes from params
        self.headless = headless
        self.timeout = timeout

        # automatically grab correct chrome driver for current chrome browser version
        chromedriver_autoinstaller.install()

        # configure chrome options
        options = webdriver.ChromeOptions()

        # specify specific location for profile data
        options.add_argument('--profile-directory=Profile 1')  # specific profile
        options.add_argument(fr"--user-data-dir={os.environ['PROFILEDATA']}")  # path to personal profile data

        # add headless argument if specified
        if headless:
            options.add_argument("--headless=new")
        else:  # maximize window
            options.add_argument("--start-maximized")

        # create driver with configured options
        super(ChromeDriver, self).__init__(options=options)

    def find(self,
             search_method: By,
             search_string: str,
             clickable: bool = False):
        """
        purpose: find an element with appropriate waits
        :param search_method: "By" selection
        :param search_string: string to search with given search_method - xpath, id, etc
        :param clickable: wait for element to be clickable if true, else waits for element to be visible
        :return element: found element
        """
        if clickable:  # wait for element to be clickable
            return WebDriverWait(self, self.timeout).until(expected_conditions.presence_of_element_located((search_method, search_string)))
        else:  # wait for element to be visible
            return WebDriverWait(self, self.timeout).until(expected_conditions.visibility_of_element_located((search_method, search_string)))