from typing import Iterable

from readers_common import GeneralReader

JACOBS_URL = "https://careers.jacobs.com/job-search-results/"


class JacobsReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = JACOBS_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            # Default parameters if none are provided
            job_titles = [
                "'Data Scientist Associate'", "'Data Scientist Lead'",
                "'Data Scientist'", "'Machine Learning'", "'Python'"
            ]
            self.parameters = [{
                'keyword': keyword,
                'location': 'Philadelphia, PA, USA',
                'latitude': '39.9525839',
                'longitude': '-75.1652215',
                'radius': '50'
            } for keyword in job_titles]

if __name__ == "__main__":
    with JacobsReader() as jr:
        jr.open_job_pages(base_url=jr.base_url, parameters=jr.parameters, testmode=jr.testmode)
        print(jr.webdriver.title)
        jr.close_with_test(testmode=False)
