import re
from time import sleep

from Data.reference_values import actual_values
from readers import GeneralReaderPlaywright
from readers.captech_playwright import CAPTECH_URL


class CaptechDepositor(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=CAPTECH_URL, testmode=testmode)
        self.rv = actual_values

    def open_location_url(self):
        """
        The purpose of this code is to open the location URL and fill in all data.

        Returns:
            None

        """
        # Get the data from the refrence values object.

        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()

        self.safe_click(page_olu.get_by_role("button", name="Accept"))
        connections_url = (
            "https://join.smartrecruiters.com/CapTechConsulting/55db2334-66b1-4e85-bba9-c9b54526f9c5-captech"
            "-connections")

        # Create a new tab and navigate to the Connections URL
        page_cc = self.create_new_tab(connections_url)
        u_ = 'input#cvUpload'
        page_cc.wait_for_selector(u_, state="visible")
        locator = page_cc.locator(u_)
        locator.set_input_files(self.rv.current_resume_path)
        sleep(1)

        # Get Location field and enter location
        location_field = page_cc.get_by_label("Location")
        self.safe_click(location_field, timeout=1000, sleep_time=1)
        location_field.type("Philade")
        sleep(3)
        page_cc.get_by_text("Philadelphia, PA, US").click()

        # accept terms.
        ppt_text = ("By checking this box, you will declare that you read and understand the privacy policy of CapTech "
                    "Consulting.")
        page_cc.get_by_label(ppt_text).check()
        page_cc.get_by_role("button", name="Next").click()

        # Wait for the new page or new form section to load
        page_cc.wait_for_selector("label:text('What is your current company?')", state="visible")

        current_co = page_cc.get_by_label("What is your current company?")
        self.click_type(current_co, input_message=self.rv.current_company, sleep_time=1)

        job_title = page_cc.get_by_label("What is your current role/job title?")
        self.click_type(job_title, input_message=self.rv.current_title, sleep_time=1)
        job_title.press("Tab")
        sleep(1)

        # Get the desired job list and click on the desired job.
        desired_job_list = [re.compile(r"^Data Analysis$"), re.compile(r"^Data Engineering$"),
                            re.compile(r"^Data Science$"), ]
        for job in desired_job_list:
            j_ = page_cc.get_by_text(job).nth(1)
            sleep(1)
            j_.click()

        page_cc.get_by_role("button", name="Sign Up").click()
        sleep(20)


with CaptechDepositor() as cd:
    cd.open_location_url()
