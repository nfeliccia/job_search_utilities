import keyring
from playwright.sync_api import Page

from common_code.workday_reader import WorkdayReader

# Constants for job categories
FLEXENTIAL_URL = "https://flexential.wd5.myworkdayjobs.com/en-US/flexential_career/login"
FLEXENTIAL_TIMEOUT = 1000
FLEXENTIAL_USERNAME = "nic@secretsmokestack.com"


class FlexentialReader(WorkdayReader):

    def __init__(self, workday_url=None, page_sleep=None, testmode: bool = False):
        super().__init__(workday_url=workday_url, testmode=testmode)

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        self.safe_click(page.get_by_role(role="button", name="Search for Jobs"))

        # Helper method to set up location
        def setup_location(search_text_sl, option_name_sl):
            self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="", )
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
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword, )
        page.get_by_role(role="button", name="Search", exact=True).click()


with FlexentialReader(workday_url=FLEXENTIAL_URL) as fr:
    # Standard password grab
    secret_password = keyring.get_password(service_name=FLEXENTIAL_URL, username=FLEXENTIAL_USERNAME, )

    # Login and get page.
    active_server_page = fr.login(username=FLEXENTIAL_USERNAME, password=secret_password, )

    # Need to press the accept cookies button
    fr.safe_click(active_server_page.get_by_role("button", name="Accept Cookies"))
    search_for_jobs = active_server_page.locator("button[data-automation-id='searchForJobsButton']")

    # move on to the search for jobs.
    fr.safe_click(search_for_jobs)
    input("Press Enter to continue...")
    fr.logout(page=active_server_page, username=FLEXENTIAL_USERNAME, )
    fr.close_with_test(testmode=fr.testmode)
