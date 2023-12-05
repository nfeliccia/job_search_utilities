import logging

from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from Source import GeneralReaderPlaywright


class BeaconHillReader(GeneralReaderPlaywright):
    BEACON_HILL_URL = "https://www.beaconhillstaffing.com/Job-Seekers/Find-a-Job"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.BEACON_HILL_URL, testmode=testmode)
        self.cookies_accepted = False

    def handle_cookies(self, page: Page = None):
        if not self.cookies_accepted:
            try:
                later_ = page.get_by_role("link", name="Later")
                self.safe_click(later_, timeout=5000)
                self.cookies_accepted = True
            except TimeoutError:
                logging.error("Failed to accept cookies.")

    def open_location_url(self):
        page_olu = self.create_new_tab()
        self.handle_cookies(page_olu)
        return page_olu

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: string. A word to search for.

        Returns:

        """
        page_sk = self.create_new_tab()
        kw_ = page_sk.get_by_placeholder("Keyword or Job Title")
        self.click_type(kw_, input_message=keyword, enter=True)
        page_sk.wait_for_selector("p.how_many_jobs_text:has-text('jobs available for search')", state="visible")
        content = page_sk.content()
        return content

    def open_all_keywords(self):
        all_keyword_pages = [self.search_keyword(keyword) for keyword in universal_search_terms]
        return all_keyword_pages


def beacon_hill_reader():
    logging.basicConfig(level=logging.INFO)
    with BeaconHillReader(testmode=False) as bhr_reader:
        bhr_reader.open_location_url()
        bhr_reader.open_all_keywords()
        bhr_reader.close_with_test(testmode=False)


if __name__ == "__main__":
    beacon_hill_reader()
