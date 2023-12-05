import logging

from Source import GeneralReaderPlaywright


class PrudentialReader(GeneralReaderPlaywright):
    prudential_primary_jobs = "https://jobs.prudential.com/us-en/"
    prudential_data_analytics_url = "https://jobs.prudential.com/us-en/job-categories/data"
    prudential_technology_page = "https://jobs.prudential.com/us-en/job-categories/technology"

    def __init__(self, testmode: bool = False, qth: str = None):
        super().__init__(root_website=self.prudential_primary_jobs, testmode=testmode)
        self.qth = qth

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
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """

        try:
            page = self.create_new_tab()
            accept_button_locator = page.locator('#onetrust-accept-btn-handler')
            self.safe_click(accept_button_locator, error_message="Accept Cookies button not found")
            jt_ok = page.locator('input[placeholder="Job Title or Keywords"]')
            self.click_type(locator=jt_ok, input_message=keyword, enter=True)
            page.wait_for_load_state('load')
            sk_content = page.content()
            return sk_content
        except Exception as e:
            logging.error(f"Failed to search keyword: {e}")


def prudential_reader(testmode: bool = False, qth: str = "Philadelphia, PA"):
    with PrudentialReader(testmode=testmode, qth=qth) as pru_reader:
        for keyword in ["Python", "Data Scientist"]:
            pru_reader.search_keyword(keyword)
        pru_reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    prudential_reader(testmode=False)
