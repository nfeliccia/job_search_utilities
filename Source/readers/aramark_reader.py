from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright

# Constants for job categories
CORPORATE_FIELD_SUPPORT = "Corporate & Field Support"
INFORMATION_TECHNOLOGY = "Information Technology"
ARAMARK_URL = "https://careers.aramark.com/search/"
ARAMARK_TIMEOUT = 1000


class AramarkReader(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=ARAMARK_URL, testmode=testmode)

    def _select_job_category(self, page: Page, category: str, error_message: str):
        l_ = "label"
        ckmk = "checkmark"
        locator_ = page.locator(l_).filter(has_text=category).get_by_label(ckmk)
        self.safe_click(locator=locator_, timeout=ARAMARK_TIMEOUT, error_message=error_message)

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
        acc_ = "Accept"
        b_ = "button"
        err_acc = "Error closing Accept popup"
        err_wc = "Error closing widget chatbox popup"
        sb_ = "searchbox"
        wcb = "widget_chatbox_popover"

        # Closing the popups
        self.click_by_role(page=page, role=b_, name=acc_, timeout=5 * ARAMARK_TIMEOUT, error_message=err_acc)
        wcp = page.get_by_test_id(wcb)
        self.click_by_label(locator=wcp, label_text="Close", timeout=ARAMARK_TIMEOUT, error_message=err_wc)

        # Fill in Keyword and location.
        self.click_by_role(page=page, role=sb_, name="What?")
        if exact:
            keyword = f'"{keyword}"'
        self.click_type(page.get_by_role(sb_, name="What?"), input_message=keyword, timeout=ARAMARK_TIMEOUT,
                        sleep_time=1)
        where_sb = page.get_by_role(sb_, name="Where?")
        where_sb.fill(qth)
        where_sb.press("Enter")
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
    with AramarkReader() as ar:
        pages_list = []
        for term in universal_search_terms:
            pages_list.append(ar.search_keyword(term, qth=qth))
        pages_list.append(ar.get_corporate_jobs(qth=qth))
        ar.close_with_test(testmode=testmode)


if __name__ == "__main__":
    aramark_reader(testmode=False)
