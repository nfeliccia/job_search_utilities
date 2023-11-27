from typing import Iterable

from readers_common_old import GeneralReader

BASE_URL = "https://motionrecruitment.com/tech-jobs"
EVENTS_URL = "https://techinmotion.com/upcoming-events"
KEYWORDS = ["Machine+Learning", "Data+Science", "Python"]


class TechInMotionReader(GeneralReader):
    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = BASE_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = [
                {"radius": "25", "search-city": "19124", "postalcode": "19124", "remote": "true", "keywords": keyword}
                for keyword in KEYWORDS
            ]

    def open_events_page(self):
        self.open_a_tab(EVENTS_URL)


if __name__ == "__main__":
    with TechInMotionReader() as timr:
        timr.open_job_pages(base_url=timr.base_url, parameters=timr.parameters)
        timr.open_events_page()  # Open the events page
        print(timr.webdriver.title)  # This will print the title of the current tab, which will be the events page
        timr.close_with_test(testmode=False)
