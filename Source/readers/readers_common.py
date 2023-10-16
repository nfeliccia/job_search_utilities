from urllib.parse import urlencode

from selenium import webdriver

"""
This module contains common functions for all readers. 
"""


def initialize_webdriver(options=None):
    """
    Initializes a Selenium WebDriver with optional settings.

    Args:
    options (webdriver.ChromeOptions, optional): Optional ChromeOptions object. Defaults to None.

    Returns:
    webdriver.Chrome: Initialized Chrome WebDriver.
    """
    # Set up the default options if none are provided
    if options is None:
        options = webdriver.ChromeOptions()
        # Add any default options you want; for example:
        # options.add_argument('--headless')

    # Initialize the WebDriver with the options
    driver = webdriver.Chrome(options=options)
    # Open a blank tab
    driver.get("about:blank")
    # Common setup for all WebDrivers
    driver.maximize_window()

    return driver


def construct_url(base_url, query_params=None):
    """
    Constructs a URL by appending query parameters to the base URL.

    Args:
    base_url (str): The base URL that the query parameters should be appended to.
    query_params (dict, optional): A dictionary containing the query parameters. Defaults to None.

    Returns:
    str: The constructed URL.
    """
    if query_params:
        # Construct the query string from the dictionary
        query_string = urlencode(query_params)

        # Append the query string to the base URL
        url = f"{base_url}?{query_string}"
    else:
        url = base_url

    return url


def close_with_test(driver=None, testmode=False):
    """
    THeh purpose of this function is to close the browser after the test is complete.
    Args:
        driver: Chrome Drive
        testmode: Boolean for test mode

    Returns:

    """
    if not testmode:
        input("Press Enter to close the browser...")

    driver.quit()
