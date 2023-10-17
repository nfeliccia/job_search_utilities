import logging
from urllib.parse import urlencode

from selenium import webdriver


class GeneralReader:

    def __init__(self):
        self.webdriver = None

    def __enter__(self):
        self.webdriver = self.start_webdriver()
        logging.info("WebDriver has started.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_webdriver()
        logging.info("WebDriver has closed.")
        if exc_type:
            # Log the exception with traceback
            logging.error("An exception occurred", exc_info=(exc_type, exc_value, traceback))
            # Or you can log the exception details explicitly
            logging.error(f"Exception type: {exc_type}, Exception value: {exc_value}, Traceback: {traceback}")

    def open_job_pages(self, base_url, parameters):
        """
        Opens job pages based on the provided base URL and query parameters. Handles cookie consent popups if necessary.

        Args:
            base_url (str): The base URL for the job search page.
            parameters (Iterable[dict]): An iterable of query parameters for URL construction.
        """
        urls = [self.construct_url(base_url=base_url, query_params=param) for param in parameters]

        for url in urls:
            self.open_a_tab(url)

    def start_webdriver(self):
        """
        Starts a new Selenium WebDriver object and maximizes the window.

        Returns:
            webdriver.Chrome: A Selenium WebDriver object.
        """

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        logging.info("WebDriver started with window maximized.")
        return driver

    def close_webdriver(self):
        if self.webdriver:
            self.webdriver.quit()
            logging.info("WebDriver has quit.")

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
        logging.info("WebDriver has quit after user prompt.")

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

        logging.info(f"URL constructed: {url}")
        return url

    def open_a_tab(self, url):
        """
        Opens just one tab.
        Args:
            url:

        Returns:

        """
        try:
            self.webdriver.execute_script(f"window.open('{url}','_blank');")
            logging.info(f"Opened a new tab with URL: {url}")
        except Exception as e:
            logging.error(f"An error occurred while opening a new tab at {url}: {e}")

    def open_a_list_of_urls_in_tabs(self, urls):
        """
        Opens a list of URLs in new browser tabs.

        Args:
            urls (list): A list of URLs to open in new tabs.

        Returns:
            None
        """
        for url in urls:
            self.open_a_tab(url=url)

    def navigate_to_page(self, url):
        try:
            self.webdriver.get(url)
            logging.info(f"Navigated to URL: {url}")
        except Exception as e:
            logging.error(f"An error occurred while navigating to {url}: {e}")

    def get_page_content(self):
        try:
            content = self.webdriver.page_source
            logging.info("Retrieved the page content.")
            return content
        except Exception as e:
            logging.error(f"An error occurred while retrieving the page content: {e}")
