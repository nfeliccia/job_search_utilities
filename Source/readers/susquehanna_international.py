from typing import Iterable

from readers_common import GeneralReader

SUSQUEHANNA_URL = "https://careers.sig.com/search-results"
SUSQUEHANNA_PARAMETERS = [
    {"keywords": '"Data Science"'},
    {"keywords": '"Machine Learning"'},
    {"keywords": '"Python"'}
]


class SusquehannaInternationalReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = SUSQUEHANNA_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = SUSQUEHANNA_PARAMETERS

if __name__ == "__main__":
    with SusquehannaInternationalReader() as sir:
        sir.open_job_pages(base_url=sir.base_url, parameters=sir.parameters, testmode=sir.testmode)
        print(sir.webdriver.title)
        sir.close_with_test(testmode=False)
