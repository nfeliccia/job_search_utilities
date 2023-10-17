from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class GeneralReader:
    """
    A class for reading web pages.

    This class provides a number of methods for constructing URLs, opening web pages, and reading the contents of web pages.

    Attributes:
        webdriver (webdriver.Chrome): A Selenium WebDriver object.
    """

    def __init__(self):
        """
        Initializes a new GeneralReader object.

        This method initializes the Selenium WebDriver object.
        """

        self.webdriver = self.start_webdriver()

    def start_webdriver(self):
        """
        Starts a new Selenium WebDriver object and maximizes the window.

        Returns:
            webdriver.Chrome: A Selenium WebDriver object.
        """

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

        return driver

    def construct_url(self, base_url, query_params=None):
        """
        Constructs a URL by appending query parameters to the base URL.

        Args:
            base_url (str): The base URL that the query parameters should be appended to.
            query_params (dict, optional): A dictionary containing the query parameters. Defaults to None.

        Returns:
            str: The constructed URL.
        """

        if query_params:
            query_string = urlencode(query_params)
            url = f"{base_url}?{query_string}"
        else:
            url = base_url

        return url

    def close_with_test(self, testmode=False):
        """
        Closes the Selenium WebDriver object.

        Args:
            testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

        Returns:
            None
        """

        if not testmode:
            input("Press Enter to close the browser...")

        self.webdriver.quit()

    def wait_for_element(self, element_locator, timeout=10):
        """
        Waits for a specific element to appear on the web page before returning.

        Args:
            element_locator (str): The locator for the element to wait for.
            timeout (int, optional): The maximum amount of time to wait in seconds. Defaults to 10.

        Raises:
            TimeoutException: If the element does not appear within the timeout period.
        """

        wait = WebDriverWait(self.webdriver, timeout)
        wait.until(lambda driver: driver.find_element(by=element_locator))

    def read_web_page(self, url):
        """
        Reads the contents of a web page.

        Args:
            url (str): The URL of the web page to read.

        Returns:
            str: The contents of the web page.
        """
        self.wait_for_element("body")
        self.webdriver.get(url)
        content = self.webdriver.page_source
        return content

    def open_a_tab(self, url):
        """
        Opens just one tab.
        Args:
            url:

        Returns:

        """
        self.webdriver.execute_script(f"window.open('{url}','_blank');")
