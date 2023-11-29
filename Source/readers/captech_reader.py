from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright



CAPTECH_URL = "https://www.captechconsulting.com/careers/current-openings/"
PHILADELPHIA = "253788"


class CaptechReader(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=CAPTECH_URL, testmode=testmode)

    def open_location_url(self):
        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()
        self.safe_click(page_olu.get_by_role("button", name="Accept"))
        page_olu.get_by_label("Locations").select_option(PHILADELPHIA)

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: string. A word to search for.

        Returns:

        """
        page_sk = self.create_new_tab()
        self.safe_click(page_sk.get_by_role("button", name="Accept"))
        self.click_type(page_sk.get_by_placeholder("Keywords"), input_message=keyword, enter=True)
        page_sk.get_by_label("Locations").select_option(PHILADELPHIA)
        page_sk.get_by_role("button", name="Search", exact=True).click()
        content = page_sk.content()
        return content

    def open_all_keywords(self):
        # Opening URLs for the specified keywords
        all_keyword_pages = [self.search_keyword(keyword) for keyword in universal_search_terms]
        return all_keyword_pages


def captech_reader(testmode: bool = False):
    with CaptechReader(testmode=testmode) as reader:
        reader.open_location_url()
        reader.open_all_keywords()
        reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    captech_reader(testmode=True)
