import logging
import re
from time import sleep

from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class CaptechReader(GeneralReaderPlaywright):
    company_name = "captech"
    CAPTECH_URL = company_data_table[company_name]["CAPTECH_URL"]
    PHILADELPHIA = company_data_table[company_name]["PHILADELPHIA"]
    captech_talent_community = company_data_table[company_name]["captech_talent_community"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.CAPTECH_URL, testmode=testmode,
                         company_name=self.company_name, customer_id=customer_id)
        self.cookies_accepted = False
        self.testmode = testmode


    def search_captech(self):
        self.open_location_url()
        self.open_all_keywords()
        self.close_with_test(testmode=self.testmode)

    def open_location_url(self):
        """
        Opens a new tab and navigates to the specified location URL. Handles cookie acceptance and
        selects the specified location from a dropdown.
        """
        page_olu = self.create_new_tab()
        try:
            if not self.cookies_accepted and page_olu.get_by_role("button", name="Accept").is_visible():
                self.safe_click(page_olu.get_by_role("button", name="Accept"))
                self.cookies_accepted = True

            location_selector = page_olu.get_by_label("Locations")
            if location_selector.is_visible():
                location_selector.select_option(self.PHILADELPHIA)
            else:
                logging.warning("Location selector not found or not visible.")
        except Exception as e:
            logging.error(f"Error occurred in open_location_url: {e}")
            # Consider how to handle the error - retry, skip, or fail the operation

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
            keyword: string. A word to search for.

        Returns:str: page content html in string form.

        """
        page_sk = self.create_new_tab()
        kw_ = page_sk.get_by_placeholder("Keywords")
        self.click_type(kw_, input_message=keyword, enter=True)
        page_sk.get_by_label("Locations").select_option(self.PHILADELPHIA)
        button_ = page_sk.get_by_role("button", name="Search", exact=True)
        self.safe_click(button_, timeout=10000)
        content = page_sk.content()
        return content

    def open_all_keywords(self):
        # Opening URLs for the specified keywords
        all_keyword_pages = []
        for keyword in self.customer_data.search_terms:
            try:
                all_keyword_pages.append(self.search_keyword(keyword))
            except Exception as e:
                logging.error(f"Failed to search for keyword: {e}")
        return all_keyword_pages

    def captech_depositor(self):

        # Create the uplaod page
        upload_page = self.create_new_tab(website=self.captech_talent_community)

        # HAndle cookie acceptance
        if not self.cookies_accepted and upload_page.get_by_role("button", name="Accept").is_visible():
            self.safe_click(upload_page.get_by_role("button", name="Accept"))
            self.cookies_accepted = True

        # Wait for the element to be visible using the specific locator
        upload_page.wait_for_selector("div.lcf-file-picker input#cvUpload", state="visible")

        # Target the element using the locator
        locator = upload_page.locator("div.lcf-file-picker input#cvUpload")

        # Set the input files
        locator.set_input_files(self.customer_data.current_resume_path)

        # Get Location field and enter location
        location_field = upload_page.get_by_label("Location")
        self.safe_click(location_field, timeout=1000)
        location_field.type("Philadelphia PA, US")

        upload_page.get_by_text("Philadelphia, PA, US").click()

        # accept terms.
        ppt_text = ("By checking this box, you will declare that you read and understand the privacy policy of CapTech "
                    "Consulting.")
        upload_page.get_by_label(ppt_text).check()
        # upload_page.get_by_role("button", name="Next").click()

        # Target the button using its class and attributes
        next_button = upload_page.locator("button.button.branded.next-button.full-width[form='lcfValidation']")

        # Click the button
        next_button.click()

        # Wait for the new page or new form section to load
        upload_page.wait_for_selector("label:text('What is your current company?')", state="visible")

        current_co = upload_page.get_by_label("What is your current company?")
        self.click_type(current_co, input_message=self.customer_data.current_company)

        job_title = upload_page.get_by_label("What is your current role/job title?")
        self.click_type(job_title, input_message=self.customer_data.current_title)
        job_title.press("Tab")

        # Get the desired job list and click on the desired job.
        desired_job_list = [re.compile(r"^Data Analysis$"), re.compile(r"^Data Engineering$"),
                            re.compile(r"^Data Science$"), ]
        for job in desired_job_list:
            j_ = upload_page.get_by_text(job).nth(1)
            sleep(1)
            j_.click()

        upload_page.get_by_role("button", name="Sign Up").click()
        sleep(3)



if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode_ = False
    cr = CaptechReader(testmode=testmode_, customer_id=nic_)
    # cr.search_captech()
    cr.captech_depositor()
