from Data.reference_values import universal_search_terms
from Source import GeneralReaderPlaywright


class MissionStaffReader(GeneralReaderPlaywright):
    """
    A specialized class for automated interactions with the Mission Staff website's careers section.

    Inherits from GeneralReaderPlaywright and provides methods for job searching and filtering.
    """

    MISSION_STAFF_URL = "https://missionstaff.com/careers/#/"

    def __init__(self, testmode: bool = False):
        """
        Initializes the MissionStaffReader instance and the underlying Playwright browser.

        :param testmode: A boolean indicating whether to launch the browser in headless mode.
        """
        super().__init__(root_website=self.MISSION_STAFF_URL, testmode=testmode)

    def search_keyword(self, keyword: str, exact: bool = False) -> str:
        """
        Performs a keyword search for job listings on the Mission Staff careers page.

        :param keyword: The keyword to search for.
        :param exact: A boolean indicating whether to perform an exact match search.
        :return: The HTML content of the page after performing the search.
        """
        page = self.create_new_tab()
        search_box = page.get_by_role("textbox", name="Keyword Search")
        self.click_type(search_box, input_message=keyword, timeout=10000)
        search_button = page.locator('button[data-automation-id="novo-search-fab"]')
        self.safe_click(search_button)
        page.wait_for_load_state('load')
        return page.content()


def mission_staff_reader():
    with MissionStaffReader(testmode=False) as msr:
        for term in universal_search_terms:
            # Mission staff doesn't like quotes in the search terms.
            term = term.replace('"', "")
            msr.search_keyword(term, exact=True)
        msr.close_with_test(testmode=msr.testmode)


if __name__ == "__main__":
    mission_staff_reader()
