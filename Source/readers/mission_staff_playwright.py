from Data.reference_values import universal_search_terms
from readers import GeneralReaderPlaywright


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

    def get_just_technology(self) -> str:
        """
        Filters job listings on the Mission Staff careers page to show only technology jobs.

        :return: The HTML content of the page after applying the technology filter.
        """
        page = self.create_new_tab()
        page.locator("label").filter(has_text="Technology (15)").locator("i").click()
        just_tech_content = page.content()
        return just_tech_content

    def get_just_pennsylvania(self) -> str:
        """
        Filters job listings on the Mission Staff careers page to show only jobs in Pennsylvania.

        :return: The HTML content of the page after applying the Pennsylvania filter.
        """
        page = self.create_new_tab()
        page.locator("label").filter(has_text="PA (1)").locator("i").click()
        just_pennsylvania_content = page.content()
        return just_pennsylvania_content

    def search_keyword(self, keyword: str, exact: bool = False) -> str:
        """
        Performs a keyword search for job listings on the Mission Staff careers page.

        :param keyword: The keyword to search for.
        :param exact: A boolean indicating whether to perform an exact match search.
        :return: The HTML content of the page after performing the search.
        """
        page = self.create_new_tab()
        role_ = "textbox"
        search_box = page.get_by_role(role_, name="Keyword Search")
        search_box.click()
        if exact:
            keyword = f'"{keyword}"'
        search_box.fill(keyword)
        search_box.press("Enter")
        return page.content()


def mission_staff_reader():
    with MissionStaffReader(testmode=False) as reader:
        print(reader.get_just_technology())
        print(reader.get_just_pennsylvania())
        for term in universal_search_terms:
            reader.search_keyword(term, exact=True)
        input("Press any key to close")


if __name__ == "__main__":
    mission_staff_reader()
