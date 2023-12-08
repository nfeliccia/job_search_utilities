import logging

from Source import GeneralReaderPlaywright


class PrudentialReader(GeneralReaderPlaywright):
    prudential_primary_jobs = "https://jobs.prudential.com/us-en/"
    prudential_data_analytics_url = "https://jobs.prudential.com/us-en/job-categories/data"
    prudential_technology_page = "https://jobs.prudential.com/us-en/job-categories/technology"

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(customer_id=customer_id, root_website=self.prudential_primary_jobs, testmode=testmode)
        self.search_all_keywords()
        self.close_with_test(testmode=testmode)

    def initial_tab(self):
        try:
            it_page = self.create_new_tab()
            icon_ = '.onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon'
            locator = it_page.locator(icon_)
            it_page.wait_for_selector(icon_)
            self.safe_click(locator=locator, error_message="Error with  the initial tab")
        except Exception as e:
            logging.error(f"Failed to initialize tab: {e}")

    def open_data_analytics_url(self):
        try:
            data_analytics_page = self.create_new_tab(website=self.prudential_data_analytics_url)
            return data_analytics_page.content()
        except Exception as e:
            logging.error(f"Failed to open data analytics URL: {e}")

    def open_technology_url(self):
        try:
            technology_page = self.create_new_tab(website=self.prudential_technology_page)
            data_analytics_management = technology_page.locator('a[href*="Data%20Analytics%20%26%20Management"]').nth(0)
            self.safe_click(locator=data_analytics_management, error_message="Error with  the tech tab")
            return technology_page.content()
        except Exception as e:
            logging.error(f"Failed to open technology URL: {e}")

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the sk_page content.
        Args:
            keyword:

        Returns:
            str: sk_page content html in string form.

        """

        try:
            sk_page = self.create_new_tab(self.prudential_primary_jobs)
            logging.info("Waiting for the cookie consent popup to be visible")
            sk_page.wait_for_selector('.onetrust-close-btn-handler', state='visible')
            logging.info("Cookie consent popup is visible")
            logging.info("Clicking the close button on the cookie consent popup")

            # Click the close button on the cookie consent popup
            sk_page.click('.onetrust-close-btn-handler')

            logging.info("Waiting for the search box to be visible")
            # Click on the wrapper to activate the select component
            sk_page.click('#react-select-2--value')

            sk_page.wait_for_selector('#react-select-2--value', state='visible')
            logging.info("Search box is visible")
            # Create a locator object for the search box using its ID

            logging.info("Filling the search box with the keyword")
            # Use the fill method to send text to the search box
            sk_page.fill('#main-search-box', keyword)
            sk_content = sk_page.content()
            return sk_content
        except Exception as e:
            logging.error(f"Failed to search keyword: {e}")

    def search_all_keywords(self):
        super().run_all_keywords(one_keyword_function=self.search_keyword)


if __name__ == "__main__":
    customer_id = "nic@secretsmokestack.com"
    testmode = False
    PrudentialReader(customer_id=customer_id, testmode=testmode)
