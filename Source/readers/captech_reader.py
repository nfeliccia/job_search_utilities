from Data.reference_values import universal_search_terms
from readers_common import GeneralReaderPlaywright


def safe_click(locator, timeout=1000, error_message="Error during click operation"):
    """Attempt to click a locator with error handling and custom timeout."""
    try:
        locator.click(timeout=timeout)
    except Exception as e:
        print(f"{error_message}: {e}")


class CaptechReader(GeneralReaderPlaywright):
    CAPTECH_URL = "https://www.captechconsulting.com/careers/current-openings/"
    PHILADELPHIA = "253788"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.CAPTECH_URL, testmode=testmode)

    def open_location_url(self):
        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()
        safe_click(page_olu.get_by_role("button", name="Accept"))
        page_olu.get_by_label("Locations").select_option(self.PHILADELPHIA)

    def search_keyword(self, keyword: str):
        page = self.create_new_tab()
        safe_click(page.get_by_role("button", name="Accept"))
        kw_ = "Keywords"
        page.get_by_placeholder(kw_).click()
        page.get_by_placeholder(kw_).fill(keyword)
        page.get_by_placeholder(kw_).press("Enter")
        page.get_by_label("Locations").select_option(self.PHILADELPHIA)
        page.get_by_role("button", name="Search", exact=True).click()
        return page.content()

    def open_all_keywords(self):
        # Opening URLs for the specified keywords
        all_keyword_pages = [self.search_keyword(keyword) for keyword in universal_search_terms]
        return all_keyword_pages

    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


if __name__ == "__main__":
    with CaptechReader(testmode=False) as reader:
        reader.open_location_url()
        reader.open_all_keywords()
        reader.close_with_test(testmode=False)
