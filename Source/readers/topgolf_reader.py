from typing import Iterable

from readers_common import GeneralReader

TOPGOLF_URL = "https://careers.topgolf.com/jobs/"
TOPGOLF_PARAMETERS = [
    {"page": "1", "categories": "Technology Innovation / IT"},
    {"lat": "40.0228352", "lng": "-75.0911", "radius": "15", "page": "1", "radiusUnit": "MILES"}
]


class TopGolfReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = TOPGOLF_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = TOPGOLF_PARAMETERS

if __name__ == "__main__":
    with TopGolfReader() as tgr:
        tgr.open_job_pages(base_url=tgr.base_url, parameters=tgr.parameters)
        tgr.close_with_test(testmode=False)
