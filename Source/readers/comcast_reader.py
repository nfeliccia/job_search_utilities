import logging

from playwright.sync_api import Page

from Source import WorkdayReader


class ComcastReader(WorkdayReader):
    # Constants for websites to use. These are the same for all instances of this class.
    COMCAST_URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/login"
    search_url = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers"
    LOCATIONS = [
        ("PA - Philadelphia, 1701 John F Kennedy Blvd", "PA - Philadelphia, 1701 John F Kennedy Blvd"),
        ("PA - Virtual - C", "PA - Virtual - C"),
        ("PA - Virtual - C+", "PA - Virtual - C+"),
        ("PA - Philadelphia, 1717 Arch St", "PA - Philadelphia, 1717 Arch St")
    ]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(workday_url=self.COMCAST_URL, testmode=testmode, customer_id=customer_id)

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
            in_page.get_by_role("option", name=option_name, exact=True).click()
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


def read_comcast(testmode: bool = False, customer_id: str = None):
    with ComcastReader(testmode=testmode, customer_id=customer_id) as cr:
        cr.login(company_name='comcast', customer_id=cr.customer_data.email)
        cr.run_all_keywords()
        cr.close_with_test(testmode=cr.testmode)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    read_comcast(testmode=False, customer_id=nic_)
