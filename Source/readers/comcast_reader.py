from time import sleep

import keyring
from playwright.sync_api import Page

from Data.reference_values import universal_search_terms, actual_values
from Source import WorkdayReader


class ComcastReader(WorkdayReader):
    # Constants for websites to use. These are the same for all instances of this class.
    COMCAST_URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/login"
    search_url = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers"

    def __init__(self, testmode: bool = False):
        super().__init__(workday_url=self.COMCAST_URL, testmode=testmode)

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        # Enter the dialog for jobs
        # self.safe_click(page.get_by_role("button", name="Search for Jobs"))
        page = self.create_new_tab(website=self.search_url)
        sleep(3)

        # Helper method to set up location
        def setup_location(search_text_sl, option_name_sl):
            page.get_by_role(role="button", name="Location").click()
            page.get_by_label("Search All Locations").fill(search_text_sl)
            try:
                page.get_by_role("option", name=option_name_sl, exact=True).click()

                button_selector = "button[data-automation-id='viewAllJobsButton']"

                # Wait for the button to be visible
                view_jobs_button = page.wait_for_selector(button_selector, state="visible")
                view_jobs_button.click()
            except TimeoutError:
                print(f"TimeoutError: {option_name_sl}")

        # Setup various locations
        locations = [
            ("PA - Philadelphia, 1701 John F Kennedy Blvd", "PA - Philadelphia, 1701 John F Kennedy Blvd"),
            ("PA - Virtual - C", "PA - Virtual - C"),
            ("PA - Virtual - C+", "PA - Virtual - C+"),
            ("PA - Philadelphia, 1717 Arch St", "PA - Philadelphia, 1717 Arch St")
        ]
        for search_text, option_name in locations:
            setup_location(search_text, option_name)

        # Enter keyword and perform search
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        page.get_by_role("button", name="Search", exact=True).click()


def read_comcast():
    with ComcastReader() as cr:
        username = actual_values.email
        secret_password = keyring.get_password(service_name=cr.COMCAST_URL, username=username)
        active_server_page = cr.login(username=username, password=secret_password)
        for keyword in universal_search_terms:
            cr.run_one_keyword(keyword=keyword)
        input("Press enter to logout")
        cr.logout(page=active_server_page, username=username)
        cr.close_with_test(testmode=cr.testmode)


if __name__ == "__main__":
    read_comcast()
