import re
from time import sleep

from playwright.sync_api import sync_playwright

from Data.reference_values import actual_values
from readers import GeneralReaderPlaywright
from readers.captech_playwright import CAPTECH_URL


class CaptechDepositor(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=CAPTECH_URL, testmode=testmode)
        self.rv = actual_values

    def open_location_url(self):

        # Get the data from the refrence values object.

        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_olu = self.create_new_tab()
        self.safe_click(page_olu.get_by_role("button", name="Accept"))
        page_olu.get_by_role("link", name="Join CapTech Connections").click(button="right")
        connections_url = (
            "https://join.smartrecruiters.com/CapTechConsulting/55db2334-66b1-4e85-bba9-c9b54526f9c5-captech"
            "-connections")

        # Create a new tab and navigate to the Connections URL
        page_cc = self.create_new_tab(connections_url)

        # Upload resume and fill out the form.
        add_resume = page_cc.get_by_label("Add your resume")
        self.safe_click(add_resume, timeout=1000, sleep_time=1)
        sleep(1)
        page_cc.get_by_label("Add your resume").set_input_files(self.rv.current_resume_path)
        sleep(1)

        # Enter First name
        first_name = page_cc.get_by_label("First Name")
        self.safe_click(first_name, timeout=1000, sleep_time=1)
        first_name.type(self.rv.first_name)
        sleep(1)

        # Enter Last Name
        last_name = page_cc.get_by_label("Last Name")
        self.safe_click(last_name.click(), timeout=1000, sleep_time=1)
        last_name.type(self.rv.last_name)
        sleep(1)

        # Enter Email
        email_ = page_cc.get_by_label("Email")
        self.safe_click(email_, timeout=1000, sleep_time=1)
        email_.type(self.rv.email)
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

        # Next Page. Enter data. Company name, job title, and skills.
        current_co = page_cc.get_by_label("What is your current company?")
        self.safe_click(current_co, timeout=1000, sleep_time=1)
        current_co.fill("Boxplot Analytics")

        job_title = page_cc.get_by_label("What is your current role/job title?")
        self.safe_click(job_title, timeout=1000, sleep_time=1)
        job_title.fill("Data Scientist")
        job_title.press("Tab")
        sleep(1)

        page_cc.locator("div").filter(has_text=re.compile(r"^Data Analysis$")).click()
        page_cc.locator("div").filter(has_text=re.compile(r"^Data Engineering$")).click()
        page_cc.locator("div").filter(has_text=re.compile(r"^Data Science$")).click()
        print("done")
        # page1.get_by_role("button", name="Sign Up").click()

    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


cd = CaptechDepositor()
cd.open_location_url()

with sync_playwright() as playwright:
    run(playwright)
