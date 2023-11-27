import keyring
from playwright.sync_api import Page

from common_code.workday_reader import WorkdayReader

# Constants for job categories
B_YOND_URL = "https://byond.wd12.myworkdayjobs.com/en-US/B-Yond/login"
B_YOND_TIMEOUT = 1000
B_YOND_USERNAME = "nic@secretsmokestack.com"
B_YOND_SLEEP = 2


class BYond(WorkdayReader):

    def __init__(self, workday_url=None, page_sleep=None, testmode: bool = False):
        super().__init__(workday_url=workday_url, testmode=testmode, page_sleep=page_sleep)

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        self.safe_click(page.get_by_role("button", name="Search for Jobs"), sleep_time=B_YOND_SLEEP)

        # Helper method to set up location
        def setup_location(search_text_sl, option_name_sl):
            self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="",
                            sleep_time=B_YOND_SLEEP)
            page.get_by_role("button", name="Location").click()
            page.get_by_label("Search All Locations").fill(search_text_sl)
            try:
                page.get_by_role("option", name=option_name_sl, exact=True).click()
            except TimeoutError:
                print(f"TimeoutError: {option_name_sl}")

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
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword,
                        sleep_time=B_YOND_SLEEP)
        page.get_by_role("button", name="Search", exact=True).click()

    def logout(self, page: Page = None):
        self.safe_click(page.get_by_role("button", name=B_YOND_USERNAME), sleep_time=B_YOND_SLEEP)
        self.safe_click(page.get_by_label("Sign Out"), sleep_time=B_YOND_SLEEP)


with BYond(workday_url=B_YOND_URL, page_sleep=B_YOND_SLEEP) as cr:
    secret_password = keyring.get_password(service_name=B_YOND_URL, username=B_YOND_USERNAME, )
    active_server_page = cr.login(username=B_YOND_USERNAME, password=secret_password, )
    search_for_jobs = active_server_page.locator("button[data-automation-id='searchForJobsButton']")
    cr.safe_click(search_for_jobs, sleep_time=B_YOND_SLEEP)
    input("Press Enter to continue...")
    cr.logout(page=active_server_page)
    cr.close_with_test(testmode=cr.testmode)
