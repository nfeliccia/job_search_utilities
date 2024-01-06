from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class CyberCodersReader(GeneralReaderPlaywright):
    company_name = "cyber_coders"
    CYBERCODERS_URL = company_data_table[company_name]["url"]
    upload_resume = company_data_table[company_name]["upload_resume"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.CYBERCODERS_URL, testmode=testmode, customer_id=customer_id,
                         company_name=self.company_name)

    def run_cybercoders(self):
        self.cyber_coders_login()
        self.run_all_keywords()
        self.close_with_test(testmode=self.testmode)

    def cyber_coders_login(self):
        secret_password = self.get_secret(company_name=self.company_name, user_id=self.customer_data.email)
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
        """
        This function searches for a keyword on the CyberCoders website.  It is called by the run_all_keywords function
        Cybercoders has a search on their man website.
        Args:
            keyword:

        Returns:

        """
        search_url = r'https://www.cybercoders.com/search/dashboard/'
        sk_page = self.create_new_tab(search_url)

        search_input = sk_page.locator("#global-search-terms")
        location_input = sk_page.locator("#global-search-location")
        self.safe_click_and_type(search_input, keyword)
        self.safe_click_and_type(locator=location_input, input_message=self.customer_data.location)
        search_button_selector = sk_page.locator("button.hidden-search-icon[type='submit']")
        self.safe_click(search_button_selector, timeout=5000)
        return sk_page

    def run_all_keywords(self):
        super().run_all_keywords(one_keyword_function=self.search_keyword)

    def resume_upload(self):
        self.cyber_coders_login()
        ru_page = self.create_new_tab(website=self.upload_resume)
        # Target the input element using its ID
        # Upload the file
        file_input = ru_page.locator("input[name='File']").nth(0)
        file_input.set_input_files(self.customer_data.current_resume_path)

        upload_input_button = ru_page.locator("#upload-input")
        self.safe_click(upload_input_button)
        self.close_with_test(testmode=self.testmode)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    ccr = CyberCodersReader(customer_id=nic_, testmode=testmode)
    ccr.run_cybercoders()
    ccr.resume_upload()
