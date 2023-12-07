import logging

from Source import WorkdayReader


class CVSReader(WorkdayReader):
    CVS_URL = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers/login"
    SEARCH_FOR_JOBS = "https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers"
    LOCATIONS = [
        ("PA - Philadelphia", "PA - Philadelphia"),
        ("PA - Work from home", "PA - Work from home"),
        ("PA - Blue Bell", "PA - Blue Bell"),
        ("Work At Home-Pennsylvania", "Work At Home-Pennsylvania")
    ]

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(workday_url=self.CVS_URL, testmode=testmode, customer_id=customer_id)

    def setup_location(self, page, search_text, option_name):
        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message="")
        self.safe_click(page.get_by_role("button", name="Location"), use_sleep=False)
        page.get_by_label("Search All Locations").fill(search_text)
        try:
            page.get_by_role(role="option", name=option_name, exact=True).click()
            button_selector = "button[data-automation-id='viewAllJobsButton']"

            # Wait for the button to be visible
            view_jobs_button = page.wait_for_selector(button_selector, state="visible")
            view_jobs_button.click()
        except TimeoutError:
            logging.error(f"TimeoutError: {option_name}")

    def run_one_keyword(self, keyword: str = None):
        """
        The purpose of this function is to run one keyword with the settings for CVS Health.
        Args:
            keyword:

        Returns:

        """
        page = self.create_new_tab(website=self.SEARCH_FOR_JOBS)
        self.safe_click(page.get_by_role("button", name="Search for Jobs"))

        for search_text, option_name in self.LOCATIONS:
            self.setup_location(page, search_text, option_name)

        self.click_type(page.get_by_placeholder("Search for jobs or keywords"), input_message=keyword)
        page.get_by_role("button", name="Search", exact=True).click()

    def run_all_keywords(self):
        """
        This calls the parent run all keywords and passes the one keyword function for CVS to it.
        Returns:

        """
        super().run_all_keywords(one_keyword_function=self.run_one_keyword)


def cvs_reader(customer_id: str = None, testmode: bool = False):
    with CVSReader(customer_id=customer_id, testmode=testmode) as cr:
        active_server_page = cr.login(company_name='cvs', customer_id=cr.customer_data.email)
        cr.run_all_keywords()
        input("Press enter to logout")
        cr.logout(page=active_server_page)
        cr.close_with_test(testmode=cr.testmode)



if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    cvs_reader(customer_id=nic_, testmode=False)
