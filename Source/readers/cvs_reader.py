import logging

from playwright.sync_api import Page

from Source import WorkdayReader
from Source.database_code.company_data_table_reader import company_data_table


class CVSReader(WorkdayReader):
    company = "cvs"
    CVS_URL = company_data_table[company]["url"]
    SEARCH_FOR_JOBS = company_data_table[company]["search_jobs"]
    LOCATIONS = company_data_table[company]["locations"]

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(workday_url=self.CVS_URL, testmode=testmode, customer_id=customer_id)
        self.run_cvs()

    def run_cvs(self):
        """
        This is the function that runs the CVS search.
        Returns:

        """
        active_server_page = self.login(company_name='cvs', customer_id=self.customer_data.email)
        self.run_all_keywords()
        input("Press enter to logout")
        self.logout(page=active_server_page)
        self.close_with_test(testmode=testmode)

    def setup_location(self, page: Page = None, search_text: str = None, option_name: str = None):
        """
        The purpose of this function is to setup the location for the CVS website, in the Workday style.
        Args:
            page:
            search_text:
            option_name:

        Returns:

        """
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="")
        self.safe_click(page.get_by_role("button", name="Location"), use_sleep=False)
        try:
            page.get_by_label("Search All Locations").fill(search_text)
            page.get_by_role(role="option", name=option_name, exact=True).click()
            button_selector = "button[data-automation-id='viewAllJobsButton']"

            # Wait for the button to be visible
            view_jobs_button = page.wait_for_selector(button_selector, state="visible")
            view_jobs_button.click()
        except TimeoutError:
            logging.error(f"TimeoutError: {option_name}")

    def search_keyword(self, keyword: str = None):
        """
        The purpose of this function is to run one keyword with the settings for CVS Health.
        Args:
            keyword:

        Returns:

        """
        page = self.create_new_tab(website=self.SEARCH_FOR_JOBS)
        self.safe_click(page.get_by_role("button", name="Search for Jobs"))

        for search_text, option_name in self.LOCATIONS:
            self.setup_location(page, search_text, option_name)

        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        page.get_by_role("button", name="Search", exact=True).click()

    def run_all_keywords(self):
        """
        This calls the parent run all keywords and passes the one keyword function for CVS to it.
        Returns:

        """
        super().run_all_keywords(one_keyword_function=self.search_keyword)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    CVSReader(customer_id=nic_, testmode=testmode)
