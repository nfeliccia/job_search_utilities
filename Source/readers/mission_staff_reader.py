from Source import GeneralReaderPlaywright


class MissionStaffReader(GeneralReaderPlaywright):
    """
    A specialized class for automated interactions with the Mission Staff website's careers section.

    Inherits from GeneralReaderPlaywright and provides methods for job searching and filtering.
    """

    MISSION_STAFF_URL = "https://missionstaff.com/careers/#/"

    def __init__(self, customer_id: str = None, testmode: bool = False):
        """
        Initializes the MissionStaffReader instance and the underlying Playwright browser.

        :param testmode: A boolean indicating whether to launch the browser in headless mode.
        """
        super().__init__(root_website=self.MISSION_STAFF_URL, customer_id=customer_id, testmode=testmode)
        self.run_all_keywords()
        self.close_with_test(testmode=testmode)

    def run_one_keyword(self, keyword: str, exact: bool = False) -> str:
        """
        Performs a keyword search for job listings on the Mission Staff careers page.

        :param keyword: The keyword to search for.
        :param exact: A boolean indicating whether to perform an exact match search.
        :return: The HTML content of the page after performing the search.
        """
        # Note mission staff doesn't like  quotes
        keyword = keyword.replace('"', "")

        # Start a new tab.
        page = self.create_new_tab()
        search_box = page.get_by_role("textbox", name="Keyword Search")
        self.click_type(search_box, input_message=keyword, timeout=10000)
        search_button = page.locator('button[data-automation-id="novo-search-fab"]')
        self.safe_click(search_button)
        page.wait_for_load_state('load')
        return page.content()

    def run_all_keywords(self, one_keyword_function=None):
        super().run_all_keywords(one_keyword_function=self.run_one_keyword)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    MissionStaffReader(customer_id=nic_, testmode=testmode)
