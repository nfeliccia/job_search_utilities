from typing import Iterable

from readers_common import GeneralReader

TANDYMTECH_URL = "https://tandymtech.com/job-seekers/tech-search-results/"
TANDYMTECH_PARAMETERS = [
    {"keyword": "Data Science"},
    {"keyword": "Machine Learning"},
    {"keyword": "Python"}
]


class TandymtechReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = TANDYMTECH_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = TANDYMTECH_PARAMETERS

if __name__ == "__main__":
    with TandymtechReader() as tr:
        tr.open_job_pages(base_url=tr.base_url, parameters=tr.parameters, testmode=tr.testmode)
        print(tr.webdriver.title)
        tr.close_with_test(testmode=False)
