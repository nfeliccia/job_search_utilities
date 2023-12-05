import keyring
from playwright.sync_api import Page

from Data.reference_values import actual_values, universal_search_terms
from common_code.workday_reader import WorkdayReader


class FlexentialReader(WorkdayReader):
    FLEXENTIAL_URL = "https://flexential.wd5.myworkdayjobs.com/en-US/flexential_career/login"

    def __init__(self, workday_url=None, testmode: bool = False):
        super().__init__(workday_url=self.FLEXENTIAL_URL, testmode=testmode)
        self.rv = actual_values
        self.universal_search_terms = universal_search_terms
        self.job_search_url = None

    def flexential_login(self) -> Page:
        """
        Login to the flexential website.
        Returns: The main page after login.

        """
        # Login and get main page.
        secret_password = keyring.get_password(service_name=self.FLEXENTIAL_URL, username=self.rv.email, )
        flexential_page = super().login(username=self.rv.email, password=secret_password)
        accept_button = flexential_page.locator('button[data-automation-id="legalNoticeAcceptButton"]')
        self.safe_click(accept_button)
        search_for_jobs = flexential_page.locator("text=Search for Jobs").nth(0)
        # move on to the search for jobs.
        self.safe_click(search_for_jobs, timeout=10000)
        self.job_search_url = flexential_page.url
        return flexential_page

    def run_one_keyword(self, page: Page = None, keyword: str = None):
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword, timeout=10000)
        self.safe_click(page.get_by_role("button", name="Search", exact=True))


def flexential_reader():
    with FlexentialReader() as fr:
        fr.flexential_login()
        for keyword in fr.universal_search_terms:
            active_server_page = fr.create_new_tab(website=fr.job_search_url)
            fr.run_one_keyword(page=active_server_page, keyword=keyword)
        fr.close_with_test(testmode=fr.testmode)


if __name__ == '__main__':
    flexential_reader()
