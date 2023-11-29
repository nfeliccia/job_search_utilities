from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright


class BeaconHillReader(GeneralReaderPlaywright):
    beacon_hill_url = "https://www.beaconhillstaffing.com/Job-Seekers/Find-a-Job"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.beacon_hill_url, testmode=testmode)

    def open_location_url(self):
        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()
        self.safe_click(page_olu.get_by_role("link", name="Later"), timeout=5000)
        return page_olu

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: string. A word to search for.

        Returns:

        """
        page_sk = self.create_new_tab()
        self.safe_click(page_sk.get_by_role("link", name="Later"), timeout=4000)
        kw_ = page_sk.get_by_placeholder("Keyword or Job Title")
        self.click_type(kw_, input_message=keyword, enter=True)
        page_sk.wait_for_selector("p.how_many_jobs_text:has-text('jobs available for search')", state="visible")
        content = page_sk.content()
        return content

    def open_all_keywords(self, in_page: Page = None):
        # Opening URLs for the specified keywords
        all_keyword_pages = [self.search_keyword(keyword) for keyword in universal_search_terms]
        return all_keyword_pages


def beacon_hill_reader():
    with BeaconHillReader(testmode=False) as bhr_reader:
        bhr_reader.open_location_url()
        bhr_reader.open_all_keywords()
        bhr_reader.close_with_test(testmode=False)


beacon_hill_reader()
