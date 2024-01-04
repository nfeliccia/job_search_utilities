import logging

from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class CaptechReader(GeneralReaderPlaywright):
    company_name = "captech"
    CAPTECH_URL = company_data_table[company_name]["CAPTECH_URL"]
    PHILADELPHIA = company_data_table[company_name]["PHILADELPHIA"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.CAPTECH_URL, testmode=testmode,
                         company_name=self.company_name, customer_id=customer_id)
        self.cookies_accepted = False
        self.testmode = testmode
        self.search_captech()

    def search_captech(self):
        self.open_location_url()
        self.open_all_keywords()
        self.close_with_test(testmode=self.testmode)

    def open_location_url(self):
        """
        Opens a new tab and navigates to the specified location URL. Handles cookie acceptance and
        selects the specified location from a dropdown.
        """
        page_olu = self.create_new_tab()
        try:
            if not self.cookies_accepted and page_olu.get_by_role("button", name="Accept").is_visible():
                self.safe_click(page_olu.get_by_role("button", name="Accept"))
                self.cookies_accepted = True

            location_selector = page_olu.get_by_label("Locations")
            if location_selector.is_visible():
                location_selector.select_option(self.PHILADELPHIA)
            else:
                logging.warning("Location selector not found or not visible.")
        except Exception as e:
            logging.error(f"Error occurred in open_location_url: {e}")
            # Consider how to handle the error - retry, skip, or fail the operation

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: string. A word to search for.

        Returns:str: page content html in string form.

        """
        page_sk = self.create_new_tab()
        kw_ = page_sk.get_by_placeholder("Keywords")
        self.click_type(kw_, input_message=keyword, enter=True)
        page_sk.get_by_label("Locations").select_option(self.PHILADELPHIA)
        button_ = page_sk.get_by_role("button", name="Search", exact=True)
        self.safe_click(button_, timeout=10000)
        content = page_sk.content()
        return content

    def open_all_keywords(self):
        # Opening URLs for the specified keywords
        all_keyword_pages = []
        for keyword in self.customer_data.search_terms:
            try:
                all_keyword_pages.append(self.search_keyword(keyword))
            except Exception as e:
                logging.error(f"Failed to search for keyword: {e}")
        return all_keyword_pages


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode_ = False
    CaptechReader(testmode=testmode_, customer_id=nic_)
