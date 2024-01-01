import logging

from playwright.sync_api import Page

from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class AramarkReader(GeneralReaderPlaywright):
    # Constants for job categories
    company_name = "aramark"
    cdt = company_data_table[company_name]

    CORPORATE_FIELD_SUPPORT = cdt["CORPORATE_FIELD_SUPPORT"]
    INFORMATION_TECHNOLOGY = cdt["INFORMATION_TECHNOLOGY"]
    ARAMARK_URL = cdt["ARAMARK_URL"]

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, company_name=self.company_name, testmode=testmode,
                         customer_id=customer_id)
        self.cookies_accepted = False
        self.chatbot_closed = False
        self.search_all_keywords()
        self.get_corporate_jobs()
        self.close_with_test(testmode=testmode)
        logging.info(f"Customer ID: {customer_id} AramarkReader closed.")

    def handle_popups(self, page: Page):
        """
        THe purpose of this function is to handle the popups that appear when you first visit the site.
        Args:
            page: Page object from playwright

        Returns:

        """
        if not self.cookies_accepted:
            accept_button = page.locator("#onetrust-accept-btn-handler")
            try:
                self.safe_click(accept_button, timeout=3000)
                self.cookies_accepted = True
            except TimeoutError:
                logging.error(f"{self.company_name} Failed to accept cookies.")

        if not self.chatbot_closed:
            chatbox_close_button = page.locator("button.ea1514")
            try:
                self.safe_click(chatbox_close_button, timeout=3000)
                self.chatbot_closed = True
            except TimeoutError:
                logging.error(f"{self.company_name} Failed to close chatbox.")

    def _select_job_category(self, page: Page, category: str, error_message: str) -> None:
        """
        Selects a job category from the list of job categories. This is used to filter the jobs.
        Aramark has a list of job categories that are checkboxes. This function will select the category
        Args:
            page: Page object from playwright
            category: name of the category to select
            error_message: error message to log if the category cannot be selected

        Returns:

        """
        locator_ = page.locator("label").filter(has_text=category).get_by_label("checkmark")
        self.safe_click(locator=locator_, error_message=error_message)

    def select_corporate_id(self, page: Page) -> str:
        """
        This is part of the custom search for Aramark. It will select the corporate and field support and
        Args:
            page: Page object from playwright

        Returns:
            str: content of the page after selecting the corporate and field support and information technology

        """
        self._select_job_category(page, self.CORPORATE_FIELD_SUPPORT,
                                  error_message="Error selecting 'Corporate & Field Support'")
        self._select_job_category(page, self.INFORMATION_TECHNOLOGY,
                                  error_message="Error selecting 'Information Technology'")
        return page.content()

    def search_keyword(self, keyword: str) -> str:
        """
        Search for a keyword. If qth is not None, then it will be used as the location.
        Args:
            keyword: keyword to search for
            qth: location to search for


        Returns:
            str: content of the page after searching for the keyword.

        """
        sk_page = self.create_new_tab()
        self.handle_popups(sk_page)
        keyword_search_box = sk_page.locator('#form-keyword-4')
        self.click_type(keyword_search_box, input_message=keyword)
        # Don't try click type here won't work.
        location_search_box = sk_page.locator('#form-location-4')
        location_search_box.fill(self.customer_data.location)
        content_ = sk_page.content()
        return content_

    def get_corporate_jobs(self) -> str:
        """
        For Aramark, I decide to look at just corporate jobs b/c the HQ is in Philadelphia.

        Returns:

        """
        page_corporate = self.create_new_tab()
        self.handle_popups(page_corporate)
        self.select_corporate_id(page_corporate)
        load_more_button = page_corporate.locator('button[name="Load More"]')

        # Handle load more if more jobs are available
        if load_more_button.is_visible():
            self.safe_click(load_more_button, timeout=3000)

        page_corporate.get_by_label("Location").fill(self.customer_data.location)
        page_corporate.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()
        content_ = page_corporate.content()
        return content_

    def search_all_keywords(self):
        super().run_all_keywords(one_keyword_function=self.search_keyword)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    AramarkReader(customer_id=nic_, testmode=testmode)
