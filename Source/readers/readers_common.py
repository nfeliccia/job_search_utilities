import logging

from playwright.sync_api import sync_playwright, Page, Locator

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class GeneralReaderPlaywright:

    @staticmethod
    def safe_click(locator, timeout=1000, error_message="Error during click operation"):
        """Attempt to click a locator with error handling and custom timeout."""
        try:
            locator.click(timeout=timeout)
        except Exception as e:
            logging.error(f"{error_message}: {e}")

    @staticmethod
    def click_by_role(page: Page, role: str = None, name: str = None, timeout=1000,
                      error_message: str = "Error during click by role operation"):
        """Click an element based on its role and name."""
        try:
            element = page.get_by_role(role, name=name)
            if element:
                element.click(timeout=timeout)
        except Exception as e:
            logging.error(f"Error during click by role operation: {e}")
            logging.error(f"{error_message}: {e}")

    @staticmethod
    def click_by_label(page: Page = None, locator: Locator = None, label_text: str = None, exact: bool = False,
                       timeout=1000,
                       error_message: str = "Error during click by label operation"):
        """
        This clicks by label for either a locator object or a page object.
        Args:
            page: Playwright Page Object
            locator: Playwright Locator Object
            label_text: Text of label
            exact: exact text to click true or false
            timeout: timeout in milliseconds
            error_message: an error message to apss along

        Returns:
            None

        """
        try:
            if locator is None:
                element = page.get_by_label(text=label_text, exact=exact)
            else:
                element = locator.get_by_label(text=label_text, exact=exact)
            if element:
                element.click(timeout=timeout)
        except Exception as e:
            logging.error(f"Error during click by role operation: {e}")
            logging.error(f"{error_message}: {e}")

    def __enter__(self):
        return self  # this is the object that will be bound to the variable in the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()  # clean up resources here

    def __init__(self, root_website: str = None, testmode: bool = False):
        self.testmode = testmode
        self.root_website = root_website
        self.playwright = None
        self.browser = None
        self.context = None
        self.setup_playwright()

    def setup_playwright(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)  # headless=False if testmode=True
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 720})

    def create_new_tab(self, website: str = None):
        if website is None:
            website = self.root_website
        page = self.context.new_page()
        page.goto(website)
        return page

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")
