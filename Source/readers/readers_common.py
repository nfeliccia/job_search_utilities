import logging
from time import sleep

from playwright.sync_api import sync_playwright, Page, Locator

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class GeneralReaderPlaywright:

    @staticmethod
    def safe_click(locator, timeout=1000, error_message="Error during click operation", sleep_time=0):
        """Attempt to click a locator with error handling and custom timeout."""
        try:
            locator.click(timeout=timeout)
        except Exception as e:
            print(f"{error_message}: {e}")
        else:
            sleep(sleep_time)

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

        # Launch the browser. If you don't need persistent user data, you can omit 'user_data_dir'
        self.browser = self.playwright.chromium.launch(headless=False)

        # Configure context options
        context_options = {
            "viewport": {'width': 1280, 'height': 720},
            # Include other context-specific settings here if needed
        }

        # Create a new context with the specified options
        self.context = self.browser.new_context(**context_options)

        # Set user preferences to disable autofill, etc. using an init script
        self.context.add_init_script("""
            const newProto = navigator.__proto__;
            delete newProto.webdriver;  // to simulate a non-automated environment
            navigator.__proto__ = newProto;

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            // Additional modifications can be added here
        """)

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

    def click_type(self, locator, input_message: str = "", timeout: int = 1000,
                   error_message: str = "Error during click operation",
                   sleep_time=0, enter=False):
        """
        The purpose of this function is to click a locator and then type something emulating a human.
        Args:
            locator:
            timeout:
            error_message:
            sleep_time:

        Returns:

        """
        try:
            self.safe_click(locator, timeout=timeout, error_message=error_message, sleep_time=sleep_time)
            locator.type(input_message)
            if enter:
                locator.press("Enter")
        except Exception as e:
            print(f"{error_message}: {e}")
        else:
            sleep(sleep_time)
