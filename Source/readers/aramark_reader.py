from typing import Iterable

from readers_common import GeneralReader

ARAMARK_URL = "https://careers.aramark.com/search"
SUPPORT = "corporate   field support"
PHL = "Philadelphia, PA"
SUBCAT = "information technology"
ARAMARK_PARAMETERS = [
    {"keyword": "", "location": PHL, "distance": 25, "category": SUPPORT, "sub_category": SUBCAT, "industry": ""},
    {"keyword": "Data Science", "location": PHL, "distance": 25, "category": SUPPORT, "type": "", "industry": ""},
    {"keyword": "Machine Learning", "location": PHL, "distance": 25, "category": "corporate   field support",
     "type": "", "industry": ""},
    {"keyword": "", "location": PHL, "distance": 25, "category": "corporate   field support",
     "sub_category": SUBCAT, "industry": ""}
]


class AramarkReader(GeneralReader):

    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()

        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = ARAMARK_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = ARAMARK_PARAMETERS


if __name__ == "__main__":
    with AramarkReader() as ar:
        ar.open_job_pages(base_url=ar.base_url, parameters=ar.parameters)
        print(ar.webdriver.title)
        ar.close_with_test(testmode=False)
