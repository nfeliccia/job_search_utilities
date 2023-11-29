from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright


class AramarkReader(GeneralReaderPlaywright):
    # Constants for job categories
    CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ARAMARK_URL = "https://careers.aramark.com/search/"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.ARAMARK_URL, testmode=testmode)

    def _select_job_category(self, page: Page, category: str, error_message: str) -> None:
        """
        The purpose of this is to select a job category for the Aramark website.
        Args:
            page:  Page object
            category:  string. The category to select.
            error_message:  string. The error message to display if the category cannot be selected.

        Returns:
            None

        """
        locator_ = page.locator("label").filter(has_text=category).get_by_label("checkmark")
        self.safe_click(locator=locator_, error_message=error_message)

    def select_corporate_id(self, page: Page) -> str:
        """
        The purpose of this is to select just corporate to see what all corporate jobs there are.
        Args:
            page:

        Returns:
            page contents as string.
        """
        self._select_job_category(page, self.CORPORATE_FIELD_SUPPORT,
                                  error_message="Error selecting 'Corporate & Field Support'")
        self._select_job_category(page, self.INFORMATION_TECHNOLOGY,
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
        # Closing the Accept popup
        # Locate the button by its ID
        accept_button = page.locator("#onetrust-accept-btn-handler")
        self.safe_click(accept_button, timeout=3000)

        # Locate the close button by its class
        chatbox_close_button = page.locator("button.ea1514")
        self.safe_click(chatbox_close_button, timeout=1000)

        # Fill in Keyword and location.
        self.click_type(page.get_by_role("searchbox", name="What?"), input_message=keyword)
        page.get_by_role("searchbox", name="Where?").fill(qth)

        content_ = page.content()
        return content_

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
        l_ = "Location"

        self.select_corporate_id(page2)
        page2.get_by_role("button", name="Load More").click()
        page2.get_by_label(l_).fill(qth)
        # self.click_type(page2.get_by_label(l_), input_message=qth, timeout=ARAMARK_TIMEOUT, sleep_time=1)
        page2.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()
        content_ = page2.content()
        return content_


def aramark_reader(qth: str = "Philadelphia, PA", testmode: bool = False):
    """
    This is the Aramark reader. It will search for the keywords and then get the corporate jobs.
    Additional logic is added just to check corporate jobs in the Philadelphia area.
    Args:
        qth:
        testmode:

    Returns:

    """
    with AramarkReader() as ar:
        pages_list = []
        for term in universal_search_terms:
            pages_list.append(ar.search_keyword(term, qth=qth))
        pages_list.append(ar.get_corporate_jobs(qth=qth))
        ar.close_with_test(testmode=testmode)


if __name__ == "__main__":
    aramark_reader(testmode=False)
