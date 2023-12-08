from Source import GeneralReaderPlaywright


class CyberCodersReader(GeneralReaderPlaywright):
    CYBERCODERS_URL = "https://www.cybercoders.com/"

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.CYBERCODERS_URL, testmode=testmode, customer_id=customer_id)

    def cyber_coders_login(self):
        company_name = 'cyber_coders'
        secret_password = self.get_secret(company_name=company_name, user_id=self.customer_data.email)
        ccl_page = self.create_new_tab()
        ddl_ = ccl_page.locator("#dropdown-login").get_by_text("Login")
        ddl_.click()

        # Email address entry
        self.safe_click_and_type(ccl_page.get_by_placeholder("Email address"), self.customer_data.email)

        # Password entry
        pwd_ = ccl_page.get_by_placeholder("Password").nth(1)
        self.safe_click_and_type(pwd_, secret_password)
        ccl_page.get_by_role("button", name="Login").click()
        ccl_page.wait_for_load_state("networkidle")
        return ccl_page

    def search_keyword(self, keyword: str):
        search_url = r'https://www.cybercoders.com/search/dashboard/'
        page = self.create_new_tab(search_url)

        search_input = page.locator("#global-search-terms")
        self.safe_click_and_type(search_input, keyword)
        location_input = page.locator("#global-search-location")
        self.safe_click_and_type(locator=location_input, input_message=self.customer_data.location)
        search_button_selector = page.locator("button.hidden-search-icon[type='submit']")
        self.safe_click(search_button_selector, timeout=5000)
        return page

    def run_all_keywords(self):
        super().run_all_keywords(one_keyword_function=self.search_keyword)


def cybercoders_reader(customer_id: str = None, testmode: bool = False):
    with CyberCodersReader(customer_id=customer_id, testmode=testmode) as cr:
        cr.cyber_coders_login()
        cr.run_all_keywords()
        cr.close_with_test(testmode=cr.testmode)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    cybercoders_reader(customer_id=nic_)
