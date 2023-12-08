import logging

from playwright.sync_api import Page

from Source import WorkdayReader


class BYond(WorkdayReader):
    B_YOND_URL = "https://byond.wd12.myworkdayjobs.com/en-US/B-Yond/login"

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(customer_id=customer_id, workday_url=self.B_YOND_URL, testmode=testmode)

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
        Search for jobs.
        Args:
            page: Playwright Page Object

        Returns:

        """
        search_for_jobs = page.locator("button[data-automation-id='navigationItem-Search for Jobs']")
        self.safe_click(search_for_jobs, timeout=3000)
        input("Look for jobs and press Enter to continue...")
        return page


def byond_reader(customer_id: str = None, testmode: bool = False):
    with BYond(customer_id=customer_id, testmode=testmode) as beyond_reader:
        active_server_page = beyond_reader.byond_login()
        beyond_reader.search_for_jobs(page=active_server_page)
        beyond_reader.logout(page=active_server_page, )
        beyond_reader.close_with_test(testmode=beyond_reader.testmode)


if __name__ == '__main__':
    byond_reader(customer_id="nic@secretsmokestack.com", testmode=False)
