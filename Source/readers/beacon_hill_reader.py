import logging

from playwright.sync_api import Page

from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class BeaconHillReader(GeneralReaderPlaywright):
    company_name = "beacon_hill"
    BEACON_HILL_URL = company_data_table[company_name]["url"]

    def __init__(self, testmode: bool = False, customer_id: str = ""):
        super().__init__(root_website=self.BEACON_HILL_URL, testmode=testmode, customer_id=customer_id)
        self.cookies_accepted = False
        self.beacon_scrape()

    def beacon_scrape(self):
        """
        Begin the scraping process.
        """
        page_olu = self.create_new_tab()
        self.handle_cookies(page_olu)
        self.open_all_keywords()
        self.close_with_test(testmode=self.testmode)

    def handle_cookies(self, page: Page):
        """
        Handles the cookie consent prompt on the page by clicking the 'Later' link.

        Args:
            page (Page): The Playwright page object on which to handle cookies.
        """
        if self.cookies_accepted:
            return

        try:
            later_link = page.get_by_role("link", name="Later")
            self.safe_click(later_link, timeout=5000)
            self.cookies_accepted = True
        except TimeoutError as e:
            logging.error(f"Timeout error occurred while trying to handle cookies: {e}")
        except Exception as e:
            logging.error(f"Error occurred while trying to handle cookies: {e}")

    def search_keyword(self, keyword: str, use_location: bool = False) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Because remote jobs aer shown we'll pass through twice. Once without location and once with location.
        Args:
            keyword: string. A word to search for.

        Returns:
            str" page content html in string form.

        """
        page_sk = self.create_new_tab()

        # Enter the Keyword or job title.
        # If we're not using location we need to hit enter, if we are we dont' hit enter. This is because
        kw_enter = not use_location
        kw_ = page_sk.get_by_placeholder("Keyword or Job Title")
        self.click_type(kw_, input_message=keyword, enter=kw_enter, timeout=2000)

        # SO this website uses the location of the browser. Just clicking in the location box loads in the location.
        if use_location:
            lm_ = page_sk.locator(".facetwp-icon.locate-me")
            kl_ = page_sk.locator(".facetwp-location")
            self.safe_click(lm_, timeout=2000)
            self.safe_click(kl_, timeout=2000)
            kl_.press("Enter")

        page_sk.wait_for_selector("p.how_many_jobs_text:has-text('jobs available for search')", state="visible")
        content = page_sk.content()
        return content

    def open_all_keywords(self) -> list:
        """
        Searches for each keyword in the customer data's search terms, both with and without location,
        and returns a list of page contents for these searches.

        Returns:
            list: A list of page contents from keyword searches.
        """
        search_terms = self.customer_data.search_terms
        all_keyword_pages = []
        for keyword in search_terms:
            try:
                # Search without location
                all_keyword_pages.append(self.search_keyword(keyword, use_location=False))
                # Search with location
                all_keyword_pages.append(self.search_keyword(keyword, use_location=True))
            except Exception as e:
                logging.error(f"Error searching for keyword '{keyword}': {e}")

        return all_keyword_pages


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    BeaconHillReader(testmode=testmode, customer_id=nic_)
