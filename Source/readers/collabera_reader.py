from Data.reference_values import universal_search_terms
from readers import GeneralReaderPlaywright

# Constants for job search
COLLABERA_URL = "https://collabera.com/job-search/"
COLLABERA_TIMEOUT = 1000


class CollaberaReader(GeneralReaderPlaywright):
    def __init__(self, testmode: bool = False, qth: str = None):
        super().__init__(root_website=COLLABERA_URL, testmode=testmode)
        self.qth = qth

    def open_location_url(self):
        page = self.create_new_tab()
        self.safe_click(page.get_by_role("button", name="Accept All"), timeout=COLLABERA_TIMEOUT)
        self.click_type(locator="Location", input_message=self.qth, timeout=COLLABERA_TIMEOUT, enter=True,
                        sleep_time=1.5)

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """
        page = self.create_new_tab()
        self.safe_click(page.get_by_role("button", name="Accept"), timeout=COLLABERA_TIMEOUT)
        self.click_type(locator=page.get_by_placeholder("Job Title or Keywords"), input_message=keyword,
                        timeout=COLLABERA_TIMEOUT, enter=True, sleep_time=1.5)
        sk_content = page.content()
        return sk_content


def collabera_reader(testmode: bool = False, qth: str = "Philadelphia, PA"):
    with CollaberaReader(testmode=testmode, qth=qth) as colab_reader:
        pages_list = []
        for keyword in universal_search_terms:
            pages_list.append(colab_reader.search_keyword(keyword))
        colab_reader.close_with_test(testmode=testmode)
        return pages_list


if __name__ == "__main__":
    collabera_reader(testmode=False)
