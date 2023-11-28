import keyring
from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import WorkdayReader

# Constants for job categories
COMCAST_URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/login"
COMCAST_TIMEOUT = 1000
COMCAST_USERNAME = "nic@secretsmokestack.com"
COMCAST_SLEEP = 2


class ComcastReader(WorkdayReader):

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=COMCAST_URL, page_sleep=COMCAST_SLEEP, testmode=testmode)



    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        self.safe_click(page.get_by_role("button", name="Search for Jobs"), sleep_time=2)

        # Helper method to set up location
        def setup_location(search_text, option_name):
            self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="", sleep_time=2)
            page.get_by_role("button", name="Location").click()
            page.get_by_label("Search All Locations").fill(search_text)
            try:
                page.get_by_role("option", name=option_name, exact=True).click()
            except TimeoutError:
                print(f"TimeoutError: {option_name}")

        # Setup various locations
        locations = [
            ("phila", "PA - Philadelphia, 1701 John F Kennedy Blvd"),
            ("PA -", "PA - Virtual - C"),
            ("PA - Virtual - ", "PA - Virtual - C+"),
            ("PA - ", "PA - Philadelphia, 1717 Arch St")
        ]
        for search_text, option_name in locations:
            setup_location(search_text, option_name)

        # Enter keyword and perform search
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword, sleep_time=2)
        page.get_by_role("button", name="Search", exact=True).click()


with ComcastReader() as cr:
    secret_password = keyring.get_password(service_name=COMCAST_URL, username=COMCAST_USERNAME)
    for keyword in universal_search_terms:
        active_server_page = cr.login(username=COMCAST_USERNAME, password=secret_password)
        cr.run_one_keyword(page=active_server_page, keyword=keyword)
        input("Press Enter to continue...")
        cr.logout(page=active_server_page, username=COMCAST_USERNAME)
    cr.close_with_test(testmode=cr.testmode)
