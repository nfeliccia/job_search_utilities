from readers_common import GeneralReader

MISSION_STAFF_URL = "https://missionstaff.com/careers/#/"


class MissionStaffReader(GeneralReader):
    def __init__(self, base_url: str = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = MISSION_STAFF_URL

    def open_base_url(self):
        self.open_a_tab(self.base_url)


if __name__ == "__main__":
    with MissionStaffReader() as msr:
        msr.open_base_url()  # This ensures the base URL is opened
        print(msr.webdriver.title)
        msr.close_with_test(testmode=False)
