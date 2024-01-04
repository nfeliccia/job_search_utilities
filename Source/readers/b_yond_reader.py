import logging

from playwright.sync_api import Page

from Source import WorkdayReader
from Source.database_code.company_data_table_reader import company_data_table


class BYondReader(WorkdayReader):
    company_name = 'b-yond'
    B_YOND_URL = company_data_table[company_name]["url"]

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(customer_id=customer_id, workday_url=self.B_YOND_URL, testmode=testmode)
        active_server_page = self.byond_login()
        self.search_for_jobs(page=active_server_page)
        self.logout(page=active_server_page, )
        self.close_with_test(testmode=testmode)

    def byond_login(self) -> Page:
        """
        Login to the byond website.
        Returns: Playwright Page Object
        """
        B_YOND_USERNAME = self.customer_data.email
        try:
            active_server_page = self.login(customer_id=B_YOND_USERNAME, company_name='b_yond')
            return active_server_page
        except Exception as e:
            logging.error(f"Failed to login: {e}")

    def search_for_jobs(self, page: Page = None) -> Page:
        """
        Byond has a simple one pager that doesen't need the more complicated logic.
        Args:
            page: Playwright Page Object

        Returns:
            Page: Playwright Page Object

        """
        search_for_jobs = page.locator("button[data-automation-id='navigationItem-Search for Jobs']")
        self.safe_click(search_for_jobs, timeout=3000)
        input("Look for jobs and press Enter to continue...")
        return page


if __name__ == '__main__':
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    BYondReader(customer_id=nic_, testmode=testmode)
