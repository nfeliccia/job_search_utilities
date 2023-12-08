import logging

from Data.reference_values import universal_search_terms
from common_code.general_reader import GeneralReaderPlaywright

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class SusquehannaInternationalReader(GeneralReaderPlaywright):
    def __init__(self, testmode: bool = False):
        super().__init__(root_website='https://careers.sig.com/', testmode=testmode)

    def open_search_tab(self):
        page = self.create_new_tab()
        return page

    def accept_cookies(self, page):
        allow_button = page.get_by_role("button", name="Allow")
        if allow_button.is_visible():
            self.safe_click(allow_button)

    def perform_search(self, page, term):
        search_input = page.get_by_placeholder("Search job title or location")
        self.safe_click(search_input)
        search_input.fill(term)

        search_button = page.get_by_label("Search", exact=True)
        self.safe_click(search_button)

    def process_results(self, page, term):
        # Logic to wait for and process search results goes here
        logging.info(f"Completed search for: {term}")

    def search_jobs(self, search_terms):
        for term in search_terms:
            page = self.open_search_tab()
            self.accept_cookies(page)
            self.perform_search(page, term)
            self.process_results(page, term)


if __name__ == '__main__':
    with SusquehannaInternationalReader(testmode=True) as reader:
        reader.search_jobs(universal_search_terms)
        reader.close_with_test()
