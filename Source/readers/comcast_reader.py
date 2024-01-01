import logging

from playwright.sync_api import Page

from Source import WorkdayReader
from database_code.company_data_table_reader import company_data_table


class ComcastReader(WorkdayReader):
    # Constants for websites to use. These are the same for all instances of this class.
    company = "comcast"

    company_ = company_data_table[company]
    COMCAST_URL = company_["COMCAST_URL"]
    search_url = company_["search_url"]
    LOCATIONS = company_["LOCATIONS"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(workday_url=self.COMCAST_URL, testmode=testmode, customer_id=customer_id)
        self.login(company_name='comcast', customer_id=self.customer_data.email)
        self.run_all_keywords()
        self.close_with_test(testmode=testmode)

    def setup_location(self, in_page: Page = None, search_text: str = None, option_name: str = None):
        """

        Args:
            in_page: A page with the locaiton drop down menu
            search_text: text to select out of menu
            option_name:

        Returns:

        """
        if in_page is None or search_text is None or option_name is None:
            logging.error("Page, search text, and option name cannot be None.")
            return

        in_page.get_by_role(role="button", name="Location").click()
        in_page.get_by_label("Search All Locations").fill(search_text)
        try:
            option_ = in_page.get_by_role("option", name=option_name, exact=True)
            self.safe_click(option_, timeout=3000, use_sleep=False)
            button_selector = "button[data-automation-id='viewAllJobsButton']"
            # Wait for the button to be visible
            view_jobs_button = in_page.wait_for_selector(button_selector, state="visible")
            view_jobs_button.click()
        except TimeoutError:
            print(f"TimeoutError: {option_name}")

    def search_keyword(self, keyword: str = None):
        # Enter the dialog for jobs
        page = self.create_new_tab(website=self.search_url)

        for search_text, option_name in self.LOCATIONS:
            self.setup_location(page, search_text, option_name)

        # Enter keyword and perform search
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        page.get_by_role("button", name="Search", exact=True).click()

    def run_all_keywords(self):
        for keyword in self.customer_data.search_terms:
            self.search_keyword(keyword=keyword)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    ComcastReader(testmode=testmode, customer_id=nic_)
