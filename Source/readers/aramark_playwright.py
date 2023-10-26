from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from readers_common import GeneralReaderPlaywright

# Constants for job categories
CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
INFORMATION_TECHNOLOGY = "Information Technology"
ARAMARK_URL = "https://careers.aramark.com/search/"


def safe_click(locator, timeout=1000, error_message="Error during click operation"):
    """Attempt to click a locator with error handling and custom timeout."""
    try:
        locator.click(timeout=timeout)
    except Exception as e:
        print(f"{error_message}: {e}")


def click_by_role(page, role, name, timeout=1000):
    """Attempt to click an element by role and name with error handling."""
    locator = page.get_by_role(role, name=name)
    safe_click(locator, timeout)


class AramarkReader(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, testmode=testmode)

    def _select_job_category(self, page: Page, category: str, error_message: str):
        l_ = "label"
        ckmk = "checkmark"
        to_ = 1000
        locator_ = page.locator(l_).filter(has_text=category).get_by_label(ckmk)
        safe_click(locator=locator_, timeout=to_, error_message=error_message)

    def select_corporate_id(self, page: Page) -> str:
        """
        The purpose of this is to select just corporate to see what all corporate jobs there are.
        Args:
            page:

        Returns:
            page contents as string.
        """
        self._select_job_category(page, CORPORATE_FIELD_SUPPORT,
                                  error_message="Error selecting 'Corporate & Field Support'")
        self._select_job_category(page, INFORMATION_TECHNOLOGY,
                                  error_message="Error selecting 'Information Technology'")
        return page.content()

    def search_keyword(self, keyword: str, qth: str = None, exact: bool = False) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: a word to search for.
            qth: location
            exact:

        Returns:
            string. HTML of the page.

        """
        page = self.create_new_tab()
        role_ = "searchbox"
        what_ = "What?"
        where_ = "Where?"

        # Closing the popups
        try:
            page.get_by_role("button", name="Accept").click(timeout=3000)
        except Exception as e:
            print(f"Error closing onetrust popup: {e}")

        try:
            page.get_by_test_id("widget_chatbox_popover").get_by_label("Close").click(timeout=2000)
        except Exception as e:
            print(f"Error closing widget chatbox popup: {e}")

        click_by_role(page, role_, what_)
        if exact:
            keyword = f'"{keyword}"'
        page.get_by_role(role_, name=what_).fill(keyword)
        click_by_role(page, role_, what_)
        page.get_by_role(role_, name=where_).fill(qth)
        page.get_by_role(role_, name=where_).press("Enter")
        return page.content()

    def search_jobs(self, qth: str, keyword_list: list[str]):
        # Opening the Aramark Website.
        page = self.create_new_tab()
        # Closing the popups
        try:
            page.locator("#onetrust-close-btn-container").get_by_label("Close").click(timeout=2000)
        except Exception as e:
            print(f"Error closing onetrust popup: {e}")

        try:
            page.get_by_test_id("widget_chatbox_popover").get_by_label("Close").click(timeout=2000)
        except Exception as e:
            print(f"Error closing widget chatbox popup: {e}")

        # One page per keyword
        for keyword in keyword_list:
            self.search_keyword(keyword, qth)

    def get_corporate_jobs(self, qth: str) -> str:
        """
        The purpose of this function is to get all the corporate jobs, but still specify area.
        Args:
            qth:

        Returns:
            string. HTML of the page.

        """
        # New Page for additional operations
        page2 = self.create_new_tab()
        self.select_corporate_id(page2)
        page2.get_by_role("button", name="Load More").click()
        page2.get_by_label("Location").click()
        page2.get_by_label("Location").fill(qth)
        page2.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()
        return page2.content()

    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


def aramark_reader(qth: str = "Philadelphia, PA", testmode: bool = False):
    with AramarkReader() as ar:
        for term in universal_search_terms:
            ar.search_keyword(term, qth=qth, exact=True)
        ar.get_corporate_jobs(qth="Philadelphia, PA")
        ar.close_with_test(testmode=testmode)


if __name__ == "__main__":
    aramark_reader(testmode=False)
