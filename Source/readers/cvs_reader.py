import keyring
from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import WorkdayReader

# Constants for job categories


CVS_USERNAME = "nic@secretsmokestack.com"


class CVSReader(WorkdayReader):
    CVS_URL = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/login"
    search_for_jobs = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers"

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=self.CVS_URL, testmode=testmode)

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        rok_page = self.create_new_tab(website=self.search_for_jobs)
        self.safe_click(rok_page.get_by_role("button", name="Search for Jobs"))

        # Helper method to set up location
        def setup_location(sl_search_text, sl_option_name):
            self.click_type(rok_page.get_by_placeholder("Search for jobs or keywords"), input_message="")
            self.safe_click(rok_page.get_by_role("button", name="Location"), use_sleep=False)
            rok_page.get_by_label("Search All Locations").fill(sl_search_text)
            try:
                rok_page.get_by_role(role="option", name=sl_option_name, exact=True).click()
            except TimeoutError:
                print(f"TimeoutError: {sl_option_name}")

        # Setup various locations
        locations = [
            ("PA - Philadelphia", "PA - Philadelphia"),
            ("PA - Work from home", "PA - Work from home"),
            ("PA - Blue Bell", "PA - Blue Bell"),
            ("Work At Home-Pennsylvania", "Work At Home-Pennsylvania")
        ]
        for search_text, option_name in locations:
            setup_location(search_text, option_name)

        # Enter keyword and perform search
        self.click_type(rok_page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        rok_page.get_by_role("button", name="Search", exact=True).click()


with CVSReader() as cr:
    secret_password = keyring.get_password(service_name=cr.CVS_URL, username=CVS_USERNAME)
    active_server_page = cr.login(username=CVS_USERNAME, password=secret_password)
    for keyword in universal_search_terms:
        cr.run_one_keyword(keyword=keyword)
    input("Press Enter to continue...")
    cr.logout(page=active_server_page, username=CVS_USERNAME)

    cr.close_with_test(testmode=cr.testmode)
