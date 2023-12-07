import logging

from Source import GeneralReaderPlaywright


class CollaberaReader(GeneralReaderPlaywright):
    COLLABERA_URL = "https://collabera.com/job-search/"

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.COLLABERA_URL, testmode=testmode, customer_id=customer_id)

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
        self.click_type(locator=page.get_by_placeholder("Job Title or Keywords"), input_message=keyword, enter=True)
        self.accept_cookies(page=page)
        sk_content = page.content()
        return sk_content

    def search_multiple_keywords(self):
        pages_list = []
        for keyword in self.customer_data.search_terms:
            pages_list.append(self.search_keyword(keyword))

        return pages_list


def collabera_reader(testmode: bool = False, customer_id: str = None, ):
    with CollaberaReader(testmode=testmode, customer_id=customer_id) as colab_reader:
        colab_reader.search_multiple_keywords()
        colab_reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    collabera_reader(testmode=False, customer_id=nic_)
