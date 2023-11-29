import datetime

import keyring
from playwright.sync_api import Page

from Data.reference_values import actual_values
from common_code import WorkdayReader

rv = actual_values

FEDEX_URL = "https://careers.fedex.com/fedex/auth/1/login"


class FedexReaderUploader(WorkdayReader):

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=FEDEX_URL, testmode=testmode)
        self.rv = actual_values

    def fedex_login(self, username: str, password: str):
        """
        The purpose of this is to login to the comcast website.
        Args:
            username: username
            password: password
        """
        fedex_page = self.create_new_tab(website=self.url)
        print(f"Logging into {self.url} {datetime.datetime.now()}")

        self.safe_click(fedex_page.get_by_role("button", name="Okay"))
        # Wait for the email to make sure fedex_page fully loaded
        fedex_page.wait_for_selector('xpath=//*[@id="mat-input-0"]', state="visible")
        print(f"Email address visible {datetime.datetime.now()}")

        self.click_type(fedex_page.get_by_label("Email"), input_message=username)
        self.click_type(fedex_page.get_by_label("Password"), input_message=password)
        self.safe_click(fedex_page.get_by_role("button", name="Log In"))
        singed_in_page = fedex_page
        return singed_in_page

    def upload_resume_for_match(self, in_page: Page):
        # Click the upload button
        in_page.get_by_label("Okay").click()
        in_page.get_by_role("button", name="Job Matching").click()
        in_page.get_by_role("button", name="Start Here").click()
        in_page.set_input_files('input[type="file"]', rv.current_resume_path)
        in_page.get_by_role("button", name="Get Jobs").click()


def fedex_reader_uploader():
    with FedexReaderUploader() as fru:
        secret_password = keyring.get_password(service_name=FEDEX_URL, username=rv.email)
        initial_page = fru.fedex_login(username=rv.email, password=secret_password)
        fru.upload_resume_for_match(in_page=initial_page)
        fru.close_with_test(testmode=fru.testmode)


if __name__ == '__main__':
    fedex_reader_uploader()
