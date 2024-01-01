import logging

from Source import GeneralReaderPlaywright
from database_code.company_data_table_reader import company_data_table


class CollaberaReader(GeneralReaderPlaywright):
    company_name = "collabera"
    COLLABERA_URL = company_data_table[company_name]["COLLABERA_URL"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.COLLABERA_URL, testmode=testmode, customer_id=customer_id)
        self.search_multiple_keywords()
        self.close_with_test(testmode=testmode)

    def accept_cookies(self, page=None):
        if page is None:
            logging.error("Page cannot be None.")
            return
        accept_button = page.locator("#wt-cli-accept-all-btn")
        if accept_button.is_visible():
            element = accept_button.element_handle()
            element.wait_for_element_state("visible")
            self.safe_click(accept_button, timeout=1000, error_message="Error during click operation")

    def open_location_url(self):
        olu_page = self.create_new_tab()
        self.accept_cookies(page=olu_page)
        self.click_type(locator="Location", input_message=self.customer_data.location, enter=True)

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """
        if not keyword:
            logging.error("Keyword cannot be None or an empty string.")
            return ""
        page = self.create_new_tab()
        jt_or_k = page.get_by_placeholder("Job Title or Keywords")
        l_ = page.locator('input[name="location"]')
        self.click_type(locator=jt_or_k, input_message=keyword, enter=False)
        self.click_type(locator=l_, input_message=self.customer_data.location, enter=True)
        self.accept_cookies(page=page)
        sk_content = page.content()
        return sk_content

    def search_multiple_keywords(self):
        pages_list = []
        for keyword in self.customer_data.search_terms:
            pages_list.append(self.search_keyword(keyword))
        return pages_list


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode_ = False
    CollaberaReader(testmode=testmode_, customer_id=nic_)
