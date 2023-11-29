import keyring

from common_code.workday_reader import WorkdayReader

# Constants for job categories
B_YOND_URL = "https://byond.wd12.myworkdayjobs.com/en-US/B-Yond/login"
B_YOND_USERNAME = "nic@secretsmokestack.com"


class BYond(WorkdayReader):

    def __init__(self, workday_url=None, page_sleep=None, testmode: bool = False):
        super().__init__(workday_url=workday_url, testmode=testmode)


def byond_reader():
    with BYond(workday_url=B_YOND_URL) as cr:
        secret_password = keyring.get_password(service_name=B_YOND_URL, username=B_YOND_USERNAME, )
        active_server_page = cr.login(username=B_YOND_USERNAME, password=secret_password, )
        search_for_jobs = active_server_page.locator("button[data-automation-id='searchForJobsButton']")
        cr.safe_click(search_for_jobs)
        input("Press Enter to continue...")
        cr.logout(page=active_server_page, username=B_YOND_USERNAME, )
        cr.close_with_test(testmode=cr.testmode)


byond_reader()
