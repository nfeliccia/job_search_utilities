import keyring
from playwright.sync_api import Page

from Source import WorkdayReader


class BYond(WorkdayReader):
    B_YOND_URL = "https://byond.wd12.myworkdayjobs.com/en-US/B-Yond/login"
    B_YOND_USERNAME = "nic@secretsmokestack.com"

    def __init__(self, workday_url=None, testmode: bool = False):
        super().__init__(workday_url=self.B_YOND_URL, testmode=testmode)

    def byond_login(self) -> Page:
        """
        Login to the byond website.
        Returns: Playwright Page Object

        """
        secret_password = keyring.get_password(service_name=self.B_YOND_URL, username=self.B_YOND_USERNAME, )
        active_server_page = self.login(username=self.B_YOND_USERNAME, password=secret_password, )
        return active_server_page

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


def byond_reader():
    with BYond() as beyond_reader:
        active_server_page = beyond_reader.byond_login()
        beyond_reader.search_for_jobs(page=active_server_page)
        beyond_reader.logout(page=active_server_page, username=beyond_reader.B_YOND_USERNAME, )
        beyond_reader.close_with_test(testmode=beyond_reader.testmode)


if __name__ == '__main__':
    byond_reader()
