from common_code.workday_reader import WorkdayReader
from database_code.company_data_table_reader import company_data_table

class FlexentialReader(WorkdayReader):
    company_name = "flexential"
    FLEXENTIAL_URL = company_data_table[company_name]["FLEXENTIAL_URL"]
    FELXENTIAL_SEARCH_URL = company_data_table[company_name]["FELXENTIAL_SEARCH_URL"]

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(workday_url=self.FLEXENTIAL_URL, testmode=testmode, customer_id=customer_id,
                         company_name=self.company_name, )
        self.flexential_login()
        self.run_all_keywords()
        self.close_with_test(testmode=testmode)

    def flexential_login(self) -> None:
        """
        Login to the flexential website.
        Returns: The main page after login.

        """
        # Login and get main page.
        flexential_page = super().login(customer_id=self.customer_data.email, company_name='flexential')

        # Accept cookies
        accept_button = flexential_page.locator('button[data-automation-id="legalNoticeAcceptButton"]')
        self.safe_click(accept_button)

        # Open up the actual search jobs.
        search_for_jobs = flexential_page.locator("text=Search for Jobs").nth(0)
        self.safe_click(search_for_jobs, timeout=10000)

    def search_keyword(self, keyword: str = None):
        sk_page = self.create_new_tab(website=self.FELXENTIAL_SEARCH_URL)
        search_for_jobs = sk_page.get_by_placeholder("Search for jobs or keywords")
        self.click_type(search_for_jobs, input_message=keyword, timeout=10000)
        sb_ = sk_page.get_by_role("button", name="Search", exact=True)
        self.safe_click(sb_, timeout=10000)

    def run_all_keywords(self):
        super().run_all_keywords(one_keyword_function=self.search_keyword)


if __name__ == '__main__':
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    FlexentialReader(customer_id=nic_, testmode=testmode)
