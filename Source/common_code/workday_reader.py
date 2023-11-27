from common_code.general_reader import GeneralReaderPlaywright


class WorkdayReader(GeneralReaderPlaywright):

    def __init__(self, workday_url: str = None, page_sleep: float = 0.0, testmode: bool = False):
        super().__init__(root_website=workday_url, testmode=testmode)
        self.url = workday_url
        self.sleep = page_sleep

    def login(self, username: str, password: str):
        """
        The purpose of this is to login to the comcast website.
        Args:
            username: username
            password: password
        """
        page = self.create_new_tab(website=self.url)
        self.click_type(page.get_by_label("Email Address"), input_message=username, sleep_time=self.sleep)
        self.click_type(page.get_by_label("Password"), input_message=password, sleep_time=self.sleep)
        self.safe_click(page.get_by_role("button", name="Sign In"), sleep_time=self.sleep)
        singed_in_page = page
        return singed_in_page
