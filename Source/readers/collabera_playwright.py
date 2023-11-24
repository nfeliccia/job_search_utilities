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
        l_ = "Location"
        page.get_by_placeholder(l_).click()
        page.get_by_placeholder(l_).fill(self.qth)
        page.get_by_placeholder(l_).press("Enter")

    def search_keyword(self, keyword: str) -> str:
        page = self.create_new_tab()
        b_ = "button"
        kw_ = "Job Title or Keywords"
        self.safe_click(page.get_by_role(b_, name="Accept"), timeout=COLLABERA_TIMEOUT)
        page.get_by_placeholder(kw_).click()
        page.get_by_placeholder(kw_).fill(keyword)
        page.get_by_role(b_, name="Search", exact=True).click()
        return page.content()


def collabera_reader(testmode: bool = False, qth: str = "Philadelphia, PA"):
    with CollaberaReader(testmode=testmode, qth=qth) as colab_reader:
        pages_list = []
        for keyword in universal_search_terms:
            pages_list.append(colab_reader.search_keyword(keyword))
        colab_reader.close_with_test(testmode=testmode)
        return pages_list


if __name__ == "__main__":
    collabera_reader(testmode=False)
