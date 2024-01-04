import json
import logging
import random
from pathlib import Path
from time import sleep

import boto3
from botocore.exceptions import ClientError
from playwright.sync_api import Locator, TimeoutError  # Assuming synchronous Playwright API
from playwright.sync_api import sync_playwright

from Source.database_code.customer_data_interface import CustomerDataInterface

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

scraping_parameters_path = Path(r".\Data\scraping_parameters_config.json")
broswer_init_script_path = Path(r".\Source\common_code\browser_init_script.js")


class GeneralReaderPlaywright:
    """
     Initialize the GeneralReaderPlaywright class.

     Args:
     - user_id (str): The ID of the user. This is used to fetch the customer data from the database.
     - root_website (str, optional): The root website that the browser will navigate to. Defaults to None.
     - testmode (bool, optional): A flag indicating if the instance is in test mode. In test mode, certain behaviors may change, such as how the browser session is closed. Defaults to False.
     - viewport (dict, optional): A dictionary specifying the size of the viewport. It should have 'width' and 'height' keys. If not provided, the default viewport size is {'width': 1280, 'height': 720}.
     """

    def __enter__(self):
        return self  # this is the object that will be bound to the variable in the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()  # clean up resources here

    def __repr__(self):
        repr_string = (f"GeneralReaderPlaywright(customer_id={self.customer_id},root_website={self.root_website}, "
                       f"testmode={self.testmode}, viewport={self.viewport})")
        return repr_string

    def __init__(self, customer_id: str, company_name: str = None, root_website: str = None, testmode: bool = False,
                 viewport: dict = None):
        self.customer_id = customer_id
        self.company_name = company_name
        self.root_website = root_website
        self.testmode = testmode
        self.viewport = viewport if viewport else {'width': 1280, 'height': 720}
        self.data_interface = CustomerDataInterface()
        self.scraping_parameters_path = scraping_parameters_path
        self.init_script_path = broswer_init_script_path

        self.setup_playwright()
        self.load_scraping_parameters()
        self.customer_data = self.data_interface.get_customer_data(customer_id=customer_id)
        self.confirm_successful_setup()

    def confirm_successful_setup(self):
        """
        This function confirms that the setup was successful by checking if the browser and context are initialized.
        If they are not, it raises an exception.
        """
        if self.browser is None or self.context is None:
            raise Exception("Browser or context not initialized.")
        logging.info("Browser and context initialized successfully.")
        logging.info(f"Customer ID: {self.customer_id} {self.company_name} initialized.")
        return True

    def load_scraping_parameters(self):
        try:
            with open(self.scraping_parameters_path, "r") as f:
                scraping_parameters = json.load(f)
            self.standard_timeout = scraping_parameters["standard_timeout"]
            self.sleep_time = scraping_parameters["standard_sleep"]
        except FileNotFoundError as e:
            logging.error(f"Scraping parameters file not found: {e}")
            raise e

    def setup_playwright(self) -> None:
        self.playwright = sync_playwright().start()

        # Launch the browser. If you don't need persistent user data, you can omit 'user_data_dir'
        self.browser = self.playwright.chromium.launch(headless=False)

        # Configure context options
        # The geolocation option is used to mock the geolocation. Some websites use the location.
        context_options = {
            "viewport": self.viewport,
            # Include other context-specific settings here if needed
            "geolocation": {'latitude': 40.04, 'longitude': -75.1},  # Mock geolocation
            "permissions": ['geolocation']  # Grant permission to access geolocation
        }
        # Create a new context with the specified options
        self.context = self.browser.new_context(**context_options)

        # Set user preferences to disable autofill, etc. using an init script
        init_script_path = Path(r"./Source/common_code/browser_init_script.js")
        with open(init_script_path, 'r') as file:
            init_script = file.read()
        self.context.add_init_script(init_script)

    def create_new_tab(self, website: str = None):
        """
        The purpose of this function is to create a new tab and navigate to a website.
        IT waits until fully loaded. It returns the page.
        Args:
            website:

        Returns:

        """
        if website is None:
            website = self.root_website
        page = self.context.new_page()
        page.goto(website)
        page.wait_for_load_state('load')
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
            input(f"Press Enter to close the browser session. {self.company_name}")
        self.close()

    def click_type(self, locator, input_message: str = "", timeout: int = 1000,
                   error_message: str = "Error during click operation", enter=False, use_sleep=True) -> None:
        """
        The purpose of this function is to click a locator and then type something emulating a human.
        Args:
            use_sleep: Wait after typing - default is True  to mimic human behavior.
            enter: press enter when done
            locator: Playwright Locator object  - this is the element to click
            timeout: Passable time out.
            error_message: Default error message to pass hing goes wrong.
            input_message: The message to type. Default is empty string.
        Returns:

        """

        try:
            self.safe_click(locator, timeout=timeout, error_message=error_message)
            locator.type(input_message)
            if enter:
                locator.press("Enter")
        except Exception as e:
            print(f"{error_message}: {e}")

        if use_sleep:
            self.vari_sleep(self.sleep_time, variance_percentage=10)

    def safe_click(self, locator: Locator, timeout=None, error_message="Error during click operation", use_sleep=True):
        """Attempt to click a locator with error handling and custom timeout."""

        if timeout is None:
            timeout = self.standard_timeout

        try:
            # Wait for the element to be visible before clicking
            locator.wait_for(state="visible", timeout=timeout)
            locator.click(timeout=timeout)
        except TimeoutError as e:
            logging.error(f"Timeout while waiting for element  {locator} to be visible: {e}")
        except Exception as e:
            logging.error(f"{error_message}: {e}")
        if use_sleep:
            self.vari_sleep(self.sleep_time, variance_percentage=10)

    def safe_click_and_type(self, locator: Locator, input_message: str = "", timeout=None,
                            error_message="Error during click and type operation", enter=False, use_sleep=True):
        """Attempt to click a locator, type a message, and optionally press Enter, with error handling and custom
        timeout."""

        if timeout is None:
            timeout = self.standard_timeout

        try:
            # Wait for the element to be visible before clicking
            locator.wait_for(state="visible", timeout=timeout)
            locator.click(timeout=timeout)
            locator.type(input_message)
            if enter:
                locator.press("Enter")
        except TimeoutError as e:
            logging.error(f"Timeout while waiting for element {locator} to be visible: {e}")
        except Exception as e:
            logging.error(f"{error_message}: {e}")
        if use_sleep:
            self.vari_sleep(self.sleep_time, variance_percentage=10)

    def get_secret(self, company_name, user_id: str = None):
        if not company_name or not user_id:
            raise ValueError("Company name and user ID must be provided")

        secret_name = f"{company_name}_{user_id}"
        region_name = "us-east-2"

        # Consider using dependency injection for the AWS client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)

        try:
            logging.info(f"Retrieving secret for '{secret_name}'...")
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            logging.error(f"Error retrieving secret: {e}")
            raise Exception(f"Error retrieving secret for {company_name}") from e

        secret = get_secret_value_response.get('SecretString')
        if not secret:
            raise Exception(f"Secret '{secret_name}' not found or has no string value")

        secret_dict = json.loads(secret)
        secret_value = secret_dict.get(secret_name)  # Consider making this key a parameter

        if secret_value is None:
            logging.warning(f"Secret '{secret_name}' does not contain the expected key.")
            return None

        logging.info(f"Successfully retrieved secret for '{secret_name}'.")
        return secret_value

    def run_all_keywords(self, one_keyword_function=None) -> None:
        """
        This function creates a global function to loop through all the keywords.
        Each website has different HTML. Therefore each website needs a different function.
        Args:
            one_keyword_function: A function unique to each website.

        Returns:

        """
        for keyword in self.customer_data.search_terms:
            one_keyword_function(keyword=keyword)

    def vari_sleep(self, base_sleep_time, variance_percentage):
        """
        Sleeps for a variable amount of time based on the base sleep time and a percentage variance.

        Args:
            base_sleep_time (float): The base amount of time to sleep in seconds. Should be non-negative.
            variance_percentage (int): The percentage of variance to apply to the base sleep time. Should be between 0 and 100.

        Note:
            If the calculated sleep time is negative, it defaults to 0.
            An extremely high variance percentage may lead to unexpectedly long sleep durations.
        """
        if base_sleep_time < 0:
            logging.warning("Base sleep time is negative. Resetting to 0.")
            base_sleep_time = 0

        if not 0 <= variance_percentage <= 100:
            logging.warning("Variance percentage is out of bounds. Resetting to a reasonable value.")
            variance_percentage = max(0, min(variance_percentage, 100))

        variance = base_sleep_time * (variance_percentage / 100)
        actual_sleep_time = int(base_sleep_time + random.uniform(-variance, variance))
        actual_sleep_time = max(0, actual_sleep_time)  # Ensure non-negative sleep time

        logging.debug(f"Sleeping for {actual_sleep_time} seconds.")
        sleep(actual_sleep_time)
