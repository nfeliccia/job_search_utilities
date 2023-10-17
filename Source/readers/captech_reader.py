from typing import Iterable

from readers_common import GeneralReader

CAPTECH_URL = "https://www.captechconsulting.com/careers/current-openings/"
CAPTECH_PARAMETERS = [
    {"keywords": "", "location": "253788", "page": "1", },
    {"keywords": "Machine Learning", "page": "1", },
    {"keywords": "Data Science", "page": "1", },
    {"keywords": "Python", "page": "1", }
]


class CapTechReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = CAPTECH_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = CAPTECH_PARAMETERS


if __name__ == "__main__":
    with CapTechReader() as cr:
        cr.open_job_pages(base_url=cr.base_url, parameters=cr.parameters, testmode=cr.testmode)
        print(cr.webdriver.title)
        cr.close_with_test(testmode=False)
