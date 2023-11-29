from time import sleep

from common_code import GeneralReaderPlaywright


class PrudentialReader(GeneralReaderPlaywright):
    prudential_primary_jobs = "https://jobs.prudential.com/us-en/"
    prudential_data_analytics_url = "https://jobs.prudential.com/us-en/job-categories/data"
    prudential_technology_page = "https://jobs.prudential.com/us-en/job-categories/technology"

    def __init__(self, testmode: bool = False, qth: str = None):
        super().__init__(root_website=self.prudential_primary_jobs, testmode=testmode)
        self.qth = qth

    def initial_tab(self):
        it_page = self.create_new_tab()
        icon_ = '.onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon'
        locator = it_page.locator(icon_)
        it_page.wait_for_selector(icon_)
        self.safe_click(locator=locator, error_message="Error with  the initial tab")

    def open_data_analytics_url(self):
        data_analytics_page = self.create_new_tab(website=self.prudential_data_analytics_url)
        return data_analytics_page.content()

    def open_technology_url(self):
        technology_page = self.create_new_tab(website=self.prudential_technology_page)
        close_button = technology_page.get_by_role("button", name="Close")
        self.safe_click(close_button, timeout=3000)
        data_analytics_management = technology_page.locator('a[href*="Data%20Analytics%20%26%20Management"]').nth(0)
        self.safe_click(locator=data_analytics_management, error_message="Error with  the tech tab")
        return technology_page.content()

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """
        page = self.create_new_tab()
        self.safe_click(page.get_by_role("button", name="Accept"), )
        self.click_type(locator=page.get_by_placeholder("Job Title or Keywords"), input_message=keyword, enter=True)
        sleep(1.5)
        sk_content = page.content()
        return sk_content


def prudential_reader(testmode: bool = False, qth: str = "Philadelphia, PA"):
    with PrudentialReader(testmode=testmode, qth=qth) as pru_reader:
        pru_reader.initial_tab()
        pru_reader.open_data_analytics_url()
        pru_reader.open_technology_url()
        pru_reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    prudential_reader(testmode=False)
