import logging
import os

from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from Source import GeneralReaderPlaywright


class AramarkReader(GeneralReaderPlaywright):
    # Constants for job categories
    CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ARAMARK_URL = "https://careers.aramark.com/search/"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, testmode=testmode)
        self.cookies_accepted = False
        self.chatbot_closed = False

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

    def search_keyword(self, keyword: str, qth: str = None) -> str:
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
        sb_what = sk_page.get_by_role("searchbox", name="What?")
        self.click_type(sb_what, input_message=keyword)
        sk_page.get_by_role("searchbox", name="Where?").fill(qth)
        content_ = sk_page.content()
        return content_

    def get_corporate_jobs(self, qth: str) -> str:
        page_corporate = self.create_new_tab()
        self.handle_popups(page_corporate)
        self.select_corporate_id(page_corporate)
        self.safe_click(page_corporate.get_by_role("button", name="Load More"), timeout=3000)
        page_corporate.get_by_label("Location").fill(qth)
        page_corporate.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()
        content_ = page_corporate.content()
        return content_


def aramark_reader(qth: str = "Philadelphia, PA", testmode: bool = False):
    os.chdir(r'F:\\job_search_utilities')
    with AramarkReader() as ar:
        pages_list = []
        for term in universal_search_terms:
            keyword_result = ar.search_keyword(term, qth=qth)
            pages_list.append(keyword_result)
        pages_list.append(ar.get_corporate_jobs(qth=qth))
        ar.close_with_test(testmode=testmode)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    aramark_reader(testmode=False)
