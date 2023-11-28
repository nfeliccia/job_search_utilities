import keyring
from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import WorkdayReader

# Constants for job categories
CVS_URL = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/login"
CVS_TIMEOUT = 1000
CVS_USERNAME = "nic@secretsmokestack.com"
CVS_SLEEP_TIME = 2


class CVSReader(WorkdayReader):

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=CVS_URL, page_sleep=CVS_SLEEP_TIME, testmode=testmode)

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        self.safe_click(page.get_by_role("button", name="Search for Jobs"), sleep_time=2)

        # Helper method to set up location
        def setup_location(sl_search_text, sl_option_name):
            self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="",
                            sleep_time=CVS_SLEEP_TIME)
            page.get_by_role(role="button", name="Location").click()
            page.get_by_label("Search All Locations").fill(sl_search_text)
            try:
                page.get_by_role(role="option", name=sl_option_name, exact=True).click()
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
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword, sleep_time=2)
        page.get_by_role("button", name="Search", exact=True).click()


with CVSReader() as cr:
    secret_password = keyring.get_password(service_name=CVS_URL, username=CVS_USERNAME)
    for keyword in universal_search_terms:
        active_server_page = cr.login(username=CVS_USERNAME, password=secret_password)
        cr.run_one_keyword(page=active_server_page, keyword=keyword)
        input("Press Enter to continue...")
        cr.logout(page=active_server_page, username=CVS_USERNAME)

    cr.close_with_test(testmode=cr.testmode)
