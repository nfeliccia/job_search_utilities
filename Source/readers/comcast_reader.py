import keyring
from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from readers import GeneralReaderPlaywright

# Constants for job categories
COMCAST_URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/login"
COMCAST_TIMEOUT = 1000
COMCAST_USERNAME = "nic@secretsmokestack.com"


class ComcastReader(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=COMCAST_URL, testmode=testmode)

    def login(self, username: str, password: str):
        """
        The purpose of this is to login to the comcast website.
        Args:           
            username: username
            password: password
        """
        page = self.create_new_tab(website=COMCAST_URL)
        self.click_type(page.get_by_label("Email Address"), input_message=username, sleep_time=2)
        self.click_type(page.get_by_label("Password"), input_message=password, sleep_time=2)
        self.safe_click(page.get_by_role("button", name="Sign In"), sleep_time=2)
        singed_in_page = page
        return singed_in_page

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

    def logout(self, page: Page = None):
        self.safe_click(page.get_by_role("button", name=COMCAST_USERNAME), sleep_time=2)
        self.safe_click(page.get_by_label("Sign Out"), sleep_time=2)


with ComcastReader() as cr:
    secret_password = keyring.get_password(service_name=COMCAST_URL, username=COMCAST_USERNAME)
    for keyword in universal_search_terms:
        active_server_page = cr.login(username=COMCAST_USERNAME, password=secret_password)
        cr.run_one_keyword(page=active_server_page, keyword=keyword)
        cr.logout(page=active_server_page)
        input("Press Enter to continue...")
    cr.close_with_test(testmode=cr.testmode)
