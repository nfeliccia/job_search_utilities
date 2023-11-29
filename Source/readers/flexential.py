import keyring

from Data.reference_values import actual_values

rv = actual_values
from common_code.workday_reader import WorkdayReader

# Constants for job categories
FLEXENTIAL_URL = "https://flexential.wd5.myworkdayjobs.com/en-US/flexential_career/login"


class FlexentialReader(WorkdayReader):

    def __init__(self, workday_url=None, page_sleep=None, testmode: bool = False):
        super().__init__(workday_url=workday_url, testmode=testmode)


def flexential_reader():
    with FlexentialReader(workday_url=FLEXENTIAL_URL) as fr:
        # Standard password grab
        secret_password = keyring.get_password(service_name=FLEXENTIAL_URL, username=rv.email, )

        # Login and get page.
        active_server_page = fr.login(username=rv.email, password=secret_password, )

        # Need to press the accept cookies button
        fr.safe_click(active_server_page.get_by_role("button", name="Accept Cookies"))
        search_for_jobs = active_server_page.locator("button[data-automation-id='searchForJobsButton']")

        # move on to the search for jobs.
        fr.safe_click(search_for_jobs)
        input("Press Enter to continue...")
        fr.logout(page=active_server_page, username=rv.email, )
        fr.close_with_test(testmode=fr.testmode)


if __name__ == '__main__':
    flexential_reader()
