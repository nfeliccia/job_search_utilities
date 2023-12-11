import logging

from playwright.sync_api import Page

from Source import GeneralReaderPlaywright


class BimboJobSearcher(GeneralReaderPlaywright):
    BIMBOURL = "https://careers.bimbobakeriesusa.com/careers"

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.BIMBOURL, testmode=testmode, customer_id=customer_id)

    def click_agree_button(self, page: Page):
        try:
            agree_button = page.locator('role=button[name="I Agree"]')
            if agree_button.is_visible():
                self.safe_click(agree_button)
            else:
                logging.warning("'I Agree' button not visible")
        except TimeoutError as e:
            logging.error(f"Timeout while waiting for 'I Agree' button: {e}")
        except Exception as e:
            logging.error(f"Unexpected error clicking on 'I Agree' button: {e}")

    def upload_for_job_check(self):
        """
        The first part here uploads the resume for the job check.
        Returns:

        """

        try:
            page_pb = self.create_new_tab()
            selector = '.dropzone-container input[type="file"]'
            page_pb.wait_for_selector(selector, state="visible")

            # If the desired input is the first one, use first=0; if it's the second one, use first=1
            locator = page_pb.locator(selector).nth(0)
            locator.set_input_files(self.customer_data.current_resume_path)
            self.click_agree_button(page_pb)
            return page_pb
        except Exception as e:
            logging.error(f"Failed to upload for job check: {e}")

    def join_talent_community(self, in_page: Page = None):
        """
        Joins the talent community.
        Args:
            in_page: Page object to interact with.
        """
        talent_community_url = "https://careers.bimbobakeriesusa.com/careers/join?domain=grupobimbo.com"
        try:
            # Reuse the existing page if it's already on the talent community URL
            talent_page = self.create_new_tab(talent_community_url)

            # Check for the "Join Talent Network" link
            join_tn_link = talent_page.query_selector('a[data-test-id="join-tn-link"]')
            if join_tn_link:
                join_tn_link.click()
                logging.info("Navigated to 'Join Talent Network'")
            else:
                logging.error("Link not found")

            # Centralize locator creation
            location_locator = talent_page.get_by_placeholder("Current Location")
            company_locator = talent_page.get_by_placeholder("Current Company")
            title_locator = talent_page.get_by_placeholder("Current Title")
            privacy_checkbox = talent_page.locator('i[data-test-id="careers-talent-network-privacy-checkbox-0"]')
            submit_button = talent_page.locator('button[data-test-id="jtn-submit-btn"]')

            # Fill in the form

            self.safe_click_and_type(locator=location_locator, input_message=self.customer_data.location)
            self.safe_click_and_type(locator=company_locator, input_message=self.customer_data.current_company)
            self.safe_click_and_type(locator=title_locator, input_message=self.customer_data.current_title)
            self.safe_click_and_type(locator=privacy_checkbox)
            self.safe_click_and_type(locator=submit_button)

            logging.info("Submitted to talent community.")

        except Exception as e:
            logging.error(f"Failed to join the talent community: {e}")


def bimbo_reader_uploader(testmode: bool = False, customer_id: str = None):
    logging.basicConfig(level=logging.INFO)
    with BimboJobSearcher(customer_id=customer_id, testmode=testmode) as bjs:
        job_check_page = bjs.upload_for_job_check()
        jtc = input("Join the talent community y/n")
        if jtc.strip().lower() == 'y':
            bjs.join_talent_community(in_page=job_check_page)
        bjs.close_with_test(testmode=testmode)


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode = False
    bimbo_reader_uploader(testmode=testmode, customer_id=nic_)
