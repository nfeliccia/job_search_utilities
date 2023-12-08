import datetime
import logging

from playwright.sync_api import Page

from Source import GeneralReaderPlaywright


class WorkdayReader(GeneralReaderPlaywright):

    def __init__(self, customer_id: str = None, workday_url: str = None, testmode: bool = False):
        super().__init__(root_website=workday_url, testmode=testmode, customer_id=customer_id)
        self.url = workday_url

    def login(self, company_name: str = None, customer_id: str = None):
        """
        The purpose of this is to login to the comcast website.
        Args:
            company_name: company name
            customer_id: username
        """
        # Get the password before creating a new tab. This is because the password is stored in the database.
        secret_password = self.get_secret(company_name=company_name, user_id=self.customer_data.email)

        page = self.create_new_tab(website=self.url)
        logging.info(f"Logging into {self.url} {datetime.datetime.now()}")


        # Wait for email address to be visible
        page.wait_for_selector("xpath=//label[text()='Email Address']", state="visible")
        logging.info(f"Email address visible {datetime.datetime.now()}")

        # Execute entry.
        self.click_type(page.get_by_label("Email Address"), input_message=customer_id, enter=True)
        self.click_type(page.get_by_label("Password"), input_message=secret_password)
        self.safe_click(page.get_by_role("button", name="Sign In"))
        singed_in_page = page
        return singed_in_page

    def logout(self, page: Page = None):
        self.safe_click(page.get_by_role("button", name=self.customer_data.email))
        self.safe_click(page.get_by_label("Sign Out"), )
