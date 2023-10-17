from typing import Iterable

from readers_common import GeneralReader  # Correcting the import statement

BIMBO_URL = "https://careers.bimbobakeriesusa.com/en-US/search"
BIMBO_PARAMETERS = parameters = [{"Keywords": '"Python"'}, {"Keywords": '"Data Science"'},
                                 {"Keywords": '"Machine Learning"'}]


class BimboReader(GeneralReader):  # Correcting the class name

    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()

        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = BIMBO_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = BIMBO_PARAMETERS


if __name__ == "__main__":
    with BimboReader() as br:
        br.open_job_pages(base_url=br.base_url, parameters=br.parameters, testmode=br.testmode)
        print(br.webdriver.title)
        br.close_with_test(testmode=False)
