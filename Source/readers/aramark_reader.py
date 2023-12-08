import logging

from playwright.sync_api import Page

from Source import GeneralReaderPlaywright


class AramarkReader(GeneralReaderPlaywright):
    # Constants for job categories
    CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ARAMARK_URL = "https://careers.aramark.com/search/"

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, testmode=testmode, customer_id=customer_id)
        self.cookies_accepted = False
        self.chatbot_closed = False
        self.search_all_keywords()
        self.get_corporate_jobs()
        self.close_with_test(testmode=testmode)

    def handle_popups(self, page: Page):
        if not self.cookies_accepted:
            accept_button = page.locator("#onetrust-accept-btn-handler")
            try:
                self.safe_click(accept_button, timeout=3000)
                self.cookies_accepted = True
            except TimeoutError:
                logging.error("Failed to accept cookies.")

        if not self.chatbot_closed:
            chatbox_close_button = page.locator("button.ea1514")
            try:
                self.safe_click(chatbox_close_button, timeout=3000)
                self.chatbot_closed = True
            except TimeoutError:
                logging.error("Failed to close chatbox.")

    def _select_job_category(self, page: Page, category: str, error_message: str) -> None:
        locator_ = page.locator("label").filter(has_text=category).get_by_label("checkmark")
        self.safe_click(locator=locator_, error_message=error_message)

    def select_corporate_id(self, page: Page) -> str:
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
        location_search_box = sk_page.locator('#form-location-4')
        qth = self.customer_data.location
        location_search_box.fill(qth)
        content_ = sk_page.content()
        return content_

    def get_corporate_jobs(self) -> str:
        """
        For Aramark, I decide to look at just corporate jobs b/c the HQ is in Philadelphia.
        Args:
            qth:

        Returns:

        """
        page_corporate = self.create_new_tab()
        self.handle_popups(page_corporate)
        self.select_corporate_id(page_corporate)
        load_more_button = page_corporate.locator('button[name="Load More"]')
        qth = self.customer_data.location
        if qth is None:
            qth = "Philadelphia, PA"

        # Handle load more if more jobs are available
        if load_more_button.is_visible():
            self.safe_click(load_more_button, timeout=3000)

        page_corporate.get_by_label("Location").fill(qth)
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
