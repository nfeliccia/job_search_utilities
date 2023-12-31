from Source import GeneralReaderPlaywright


class CaptechReader(GeneralReaderPlaywright):
    CAPTECH_URL = "https://www.captechconsulting.com/careers/current-openings/"
    PHILADELPHIA = "253788"
    company_name = "captech"

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.CAPTECH_URL, testmode=testmode,
                         company_name=self.company_name, customer_id=customer_id)
        self.cookies_accepted = False
        self.open_location_url()
        self.open_all_keywords()
        self.close_with_test(testmode=testmode)

    def open_location_url(self):
        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()
        if not self.cookies_accepted:
            self.safe_click(page_olu.get_by_role("button", name="Accept"))
        page_olu.get_by_label("Locations").select_option(self.PHILADELPHIA)

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
        all_keyword_pages = [self.search_keyword(keyword) for keyword in self.customer_data.search_terms]
        return all_keyword_pages


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode_ = False
    CaptechReader(testmode=testmode_, customer_id=nic_)
