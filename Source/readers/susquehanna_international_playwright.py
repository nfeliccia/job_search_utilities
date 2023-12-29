import logging

from common_code.general_reader import GeneralReaderPlaywright

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class SusquehannaInternationalReader(GeneralReaderPlaywright):
    company_name = "Susquehanna International"
    company_website = 'https://careers.sig.com/'

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.company_website, company_name=self.company_name, testmode=testmode,
                         customer_id=customer_id)
        self.run_all_keywords()
        self.close_with_test(testmode=testmode)

    def run_one_keyword(self, keyword: str):
        page = self.create_new_tab()
        # First handle the cookies.
        allow_button = page.get_by_role("button", name="Allow")
        if allow_button.is_visible():
            self.safe_click(allow_button)

        search_input = page.get_by_placeholder("Search job title or location")
        self.click_type(search_input, keyword, timeout=3000)
        search_button = page.get_by_label("Search", exact=True)
        self.safe_click(search_button)
        page.wait_for_load_state('load')
        # Logic to wait for and process search results goes here
        logging.info(f"Completed search for: {keyword}")

    def run_all_keywords(self, one_keyword_function=None):
        super().run_all_keywords(one_keyword_function=self.run_one_keyword)


if __name__ == '__main__':
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    SusquehannaInternationalReader(testmode=testmode, customer_id=nic_)
