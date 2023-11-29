import datetime
import logging

from playwright.sync_api import Page

from common_code import GeneralReaderPlaywright


class WorkdayReader(GeneralReaderPlaywright):

    def __init__(self, workday_url: str = None, testmode: bool = False):
        super().__init__(root_website=workday_url, testmode=testmode)
        self.url = workday_url

    def login(self, username: str, password: str):
        """
        The purpose of this is to login to the comcast website.
        Args:
            username: username
            password: password
        """
        page = self.create_new_tab(website=self.url)
        logging.info(f"Logging into {self.url} {datetime.datetime.now()}")

        # Wait for the email to make sure page fully loaded
        page.wait_for_selector("xpath=//label[text()='Email Address']", state="visible")

        logging.info(f"Email address visible {datetime.datetime.now()}")
        self.click_type(page.get_by_label("Email Address"), input_message=username)
        self.click_type(page.get_by_label("Password"), input_message=password)
        self.safe_click(page.get_by_role("button", name="Sign In"))
        singed_in_page = page
        return singed_in_page

    def logout(self, page: Page = None, username: str = None):
        self.safe_click(page.get_by_role("button", name=username))
        self.safe_click(page.get_by_label("Sign Out"), )
