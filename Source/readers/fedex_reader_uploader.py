import datetime

from playwright.sync_api import Page

from Source import WorkdayReader


class FedexReaderUploader(WorkdayReader):
    FEDEX_URL = "https://careers.fedex.com/fedex/auth/1/login"

    def __init__(self, customer_id=None, testmode: bool = False):
        super().__init__(customer_id=customer_id, testmode=testmode, workday_url=self.FEDEX_URL, )

    def fedex_login(self):
        """
        The purpose of this is to login to the comcast website.
        Args:

        """
        fedex_page = self.create_new_tab(website=self.url)
        password = self.get_secret(company_name="fedex", user_id=self.customer_data.email)
        print(f"Logging into {self.url} {datetime.datetime.now()}")

        self.safe_click(fedex_page.get_by_role("button", name="Okay"), timeout=3000)
        # Wait for the email to make sure fedex_page fully loaded
        fedex_page.wait_for_selector('xpath=//*[@id="mat-input-0"]', state="visible")
        print(f"Email address visible {datetime.datetime.now()}")

        self.click_type(fedex_page.get_by_label("Email"), input_message=self.customer_data.email)
        self.click_type(fedex_page.get_by_label("Password"), input_message=password)
        self.safe_click(fedex_page.get_by_role("button", name="Log In"))
        singed_in_page = fedex_page
        return singed_in_page

    def upload_resume_for_match(self, in_page: Page):
        # Click the upload button
        ok_button = in_page.get_by_role("button", name="Okay")
        self.safe_click(ok_button, timeout=3000)
        in_page.get_by_role(role="button", name="Job Matching").click()
        in_page.get_by_role(role="button", name="Start Here").click()
        in_page.set_input_files(selector='input[type="file"]', files=self.customer_data.current_resume_path)
        in_page.get_by_role(role="button", name="Get Jobs").click()


def fedex_reader_uploader(customer_id: str = None, testmode: bool = False):
    with FedexReaderUploader(customer_id=customer_id, testmode=testmode) as fru:
        initial_page = fru.fedex_login()
        fru.upload_resume_for_match(in_page=initial_page)
        fru.close_with_test(testmode=fru.testmode)


if __name__ == '__main__':
    nic_ = "nic@secretsmokestack.com"
    fedex_reader_uploader(customer_id=nic_, testmode=False)
