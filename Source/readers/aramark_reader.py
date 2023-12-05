# This is the reader for the Aramark website. It will search for the keywords and then get the corporate jobs.cd .
import sys

sys.path.append(r'F:\job_search_utilities\\')
sys.path.append(r'F:\job_search_utilities\Source')
sys.path.append(r'F:\job_search_utilities\Source\common_code')
import os

from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from Source.common_code import GeneralReaderPlaywright


class AramarkReader(GeneralReaderPlaywright):
    # Constants for job categories
    CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ARAMARK_URL = "https://careers.aramark.com/search/"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, testmode=testmode)
        self.cookies_accepted = False
        self.chatbot_closed = False

    def _select_job_category(self, page: Page, category: str, error_message: str) -> None:
        """
        The purpose of this is to select a job category for the Aramark website.
        Args:
            page:  Page object
            category:  string. The category to select.
            error_message:  string. The error message to display if the category cannot be selected.

        Returns:
            None

        """
        locator_ = page.locator("label").filter(has_text=category).get_by_label("checkmark")
        self.safe_click(locator=locator_, error_message=error_message)

    def select_corporate_id(self, page: Page) -> str:
        """
        The purpose of this is to select just corporate to see what all corporate jobs there are.
        Args:
            page:

        Returns:
            page contents as string.
        """
        self._select_job_category(page, self.CORPORATE_FIELD_SUPPORT,
                                  error_message="Error selecting 'Corporate & Field Support'")
        self._select_job_category(page, self.INFORMATION_TECHNOLOGY,
                                  error_message="Error selecting 'Information Technology'")
        return page.content()

    def search_keyword(self, keyword: str, qth: str = None, exact: bool = False) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: a word to search for.
            qth: location
            exact:

        Returns:
            string. HTML of the sk_page.

        """
        sk_page = self.create_new_tab()
        # Closing the Accept popup
        # Locate the button by its ID
        if not self.cookies_accepted:
            accept_button = sk_page.locator("#onetrust-accept-btn-handler")
            try:
                self.safe_click(accept_button, timeout=3000)
                self.cookies_accepted = True
            except TimeoutError:
                print("Cookies already accepted.")

        # Locate the close button by its class
        if not self.chatbot_closed:
            chatbox_close_button = sk_page.locator("button.ea1514")
            try:
                self.safe_click(chatbox_close_button, timeout=3000)
                self.chatbot_closed = True
            except TimeoutError:
                print("Chatbox already closed.")

        # Fill in Keyword and location.
        self.click_type(sk_page.get_by_role("searchbox", name="What?"), input_message=keyword)
        sk_page.get_by_role("searchbox", name="Where?").fill(qth)

        content_ = sk_page.content()
        return content_

    def get_corporate_jobs(self, qth: str) -> str:
        """
        The purpose of this function is to get all the corporate jobs, but still specify area.
        Args:
            qth:

        Returns:
            string. HTML of the page.

        """
        # New Page for additional operations
        page_corporate = self.create_new_tab()

        self.select_corporate_id(page_corporate)
        self.safe_click(page_corporate.get_by_role("button", name="Load More"), timeout=3000)

        # Don't change this. FOr some reason the website doesn't like it if you use the clicktype
        page_corporate.get_by_label("Location").fill(qth)
        page_corporate.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()
        content_ = page_corporate.content()
        return content_


def aramark_reader(qth: str = "Philadelphia, PA", testmode: bool = False):
    """
    This is the Aramark reader. It will search for the keywords and then get the corporate jobs.
    Additional logic is added just to check corporate jobs in the Philadelphia area.
    Args:
        qth: Location to search for.
        testmode: If True, will not close the browser.

    Returns:

    """
    os.chdir(r'F:\\job_search_utilities')
    with AramarkReader() as ar:
        pages_list = []
        for term in universal_search_terms:
            pages_list.append(ar.search_keyword(term, qth=qth))
        pages_list.append(ar.get_corporate_jobs(qth=qth))
        ar.close_with_test(testmode=testmode)


if __name__ == "__main__":
    aramark_reader(testmode=False)
