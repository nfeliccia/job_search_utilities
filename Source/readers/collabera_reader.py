from typing import Iterable

from readers_common_old import GeneralReader

COLLABERA_URL = "https://www.collabera.com/find-a-job/search-jobs/"
COLLABERA_PARAMETERS = [
    {
        "sort_by": "",  # Specify sorting if needed
        "industry": "",  # Specify industry if needed
        "keyword": '"Python"',
        "location": "",  # Specify location if needed
        "Posteddays": "0"  # Jobs posted any time
    },
    {
        "sort_by": "",
        "industry": "",
        "keyword": '"Data Science"',
        "location": "",
        "Posteddays": "0"
    },
    {
        "sort_by": "",
        "industry": "",
        "keyword": '"Machine Learning"',
        "location": "",
        "Posteddays": "0"
    }
]


class CollaberaReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = COLLABERA_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = COLLABERA_PARAMETERS


if __name__ == "__main__":
    with CollaberaReader() as cr:
        cr.open_job_pages(base_url=cr.base_url, parameters=cr.parameters, testmode=cr.testmode)
        print(cr.webdriver.title)
        cr.close_with_test(testmode=False)
