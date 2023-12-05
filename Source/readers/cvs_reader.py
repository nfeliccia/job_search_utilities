import logging

import keyring

from Data.reference_values import universal_search_terms
from Source import WorkdayReader

CVS_USERNAME = "nic@secretsmokestack.com"


class CVSReader(WorkdayReader):
    CVS_URL = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/login"
    SEARCH_FOR_JOBS = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers"
    LOCATIONS = [
        ("PA - Philadelphia", "PA - Philadelphia"),
        ("PA - Work from home", "PA - Work from home"),
        ("PA - Blue Bell", "PA - Blue Bell"),
        ("Work At Home-Pennsylvania", "Work At Home-Pennsylvania")
    ]

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=self.CVS_URL, testmode=testmode)

    def setup_location(self, page, search_text, option_name):
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="")
        self.safe_click(page.get_by_role("button", name="Location"), use_sleep=False)
        page.get_by_label("Search All Locations").fill(search_text)
        try:
            page.get_by_role(role="option", name=option_name, exact=True).click()
            button_selector = "button[data-automation-id='viewAllJobsButton']"

            # Wait for the button to be visible
            view_jobs_button = page.wait_for_selector(button_selector, state="visible")
            view_jobs_button.click()
        except TimeoutError:
            logging.error(f"TimeoutError: {option_name}")

    def run_one_keyword(self, keyword: str = None):
        page = self.create_new_tab(website=self.SEARCH_FOR_JOBS)
        self.safe_click(page.get_by_role("button", name="Search for Jobs"))

        for search_text, option_name in self.LOCATIONS:
            self.setup_location(page, search_text, option_name)

        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        page.get_by_role("button", name="Search", exact=True).click()


def cvs_reader():
    with CVSReader() as cr:
        secret_password = keyring.get_password(service_name=cr.CVS_URL, username=CVS_USERNAME)
        active_server_page = cr.login(username=CVS_USERNAME, password=secret_password)
        for keyword in universal_search_terms:
            cr.run_one_keyword(keyword=keyword)
        input("Press Enter to continue...")
        cr.logout(page=active_server_page, username=CVS_USERNAME)

        cr.close_with_test(testmode=cr.testmode)


if __name__ == "__main__":
    cvs_reader()
