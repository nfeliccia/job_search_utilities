import sys

sys.path.append(r'F:\job_search_utilities\\')
sys.path.append(r'F:\job_search_utilities\Source')
sys.path.append(r'F:\job_search_utilities\Source\common_code')

from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright


class CollaberaReader(GeneralReaderPlaywright):
    COLLABERA_URL = "https://collabera.com/job-search/"

    def __init__(self, testmode: bool = False, qth: str = None):
        super().__init__(root_website=self.COLLABERA_URL, testmode=testmode)
        self.qth = qth

    def open_location_url(self):
        page = self.create_new_tab()
        accept_all_button = page.locator("a[id='wt-cli-accept-all-btn']")
        self.safe_click(accept_all_button)
        self.click_type(locator="Location", input_message=self.qth, enter=True)

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """
        page = self.create_new_tab()
        self.click_type(locator=page.get_by_placeholder("Job Title or Keywords"), input_message=keyword, enter=True)
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
