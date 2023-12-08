import logging

from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from Source import GeneralReaderPlaywright


class BeaconHillReader(GeneralReaderPlaywright):
    BEACON_HILL_URL = "https://www.beaconhillstaffing.com/Job-Seekers/Find-a-Job"

    def __init__(self, testmode: bool = False, customer_id: str = ""):
        super().__init__(root_website=self.BEACON_HILL_URL, testmode=testmode, customer_id=customer_id)
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

    def search_keyword(self, keyword: str, use_location: bool = False) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Becuase remote jobs aer shown we'll pass through twice. Once without location and once with location.
        Args:
            keyword: string. A word to search for.

        Returns:

        """
        page_sk = self.create_new_tab()

        # Enter the Keyword or job title.
        # If we're not using location we need to hit enter, if we are we dont' hit enter. This is because
        kw_enter = not use_location
        kw_ = page_sk.get_by_placeholder("Keyword or Job Title")
        self.click_type(kw_, input_message=keyword, enter=kw_enter, timeout=2000)

        if use_location:
            lm_ = page_sk.locator(".facetwp-icon.locate-me")
            self.safe_click(lm_, timeout=2000)
            kl_ = page_sk.locator(".facetwp-location")
            self.click_type(kl_, input_message=self.customer_data.location, enter=True, timeout=2000)

        page_sk.wait_for_selector("p.how_many_jobs_text:has-text('jobs available for search')", state="visible")
        content = page_sk.content()
        return content

    def open_all_keywords(self):
        all_keyword_pages = [self.search_keyword(keyword, use_location=False) for keyword in universal_search_terms]
        more_keyword_pages = [self.search_keyword(keyword, use_location=True) for keyword in universal_search_terms]
        all_keyword_pages.extend(more_keyword_pages)
        return all_keyword_pages


def beacon_hill_reader(customer_id: str = ""):
    logging.basicConfig(level=logging.INFO)
    with BeaconHillReader(testmode=False, customer_id=customer_id) as bhr_reader:
        bhr_reader.open_location_url()
        bhr_reader.open_all_keywords()
        bhr_reader.close_with_test(testmode=False)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    beacon_hill_reader(customer_id=nic_)
