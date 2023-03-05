#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""main.py: high level selenium navigation logic"""

__author__ = "Travis Mann"
__version__ = "0.1"
__maintainer__ = "Travis Mann"
__email__ = "tmann.eng@gmail.com"
__status__ = "Development"


# --- imports ---
from epic_driver import *


# --- main ---
if __name__ == "__main__":
    # initialize driver
    ED = EpicDriver()
    ED.claim()

    # pause for user validation
    input("validate free item redeemed (click enter to continue)...")

    # clean up resources
    ED.close()
