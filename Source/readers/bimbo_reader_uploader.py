import logging

from playwright.sync_api import Page

from Data.reference_values import actual_values
from Source import GeneralReaderPlaywright


class BimboJobSearcher(GeneralReaderPlaywright):
    BIMBOURL = "https://careers.bimbobakeriesusa.com/careers"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.BIMBOURL, testmode=testmode)
        self.rv = actual_values

    def click_agree_button(self, page: Page):
        try:
            agree_button = page.locator('role=button[name="I Agree"]')
            self.safe_click(agree_button)
        except Exception as e:
            logging.error(f"Failed to click on 'I Agree' button: {e}")

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
            locator.set_input_files(self.rv.current_resume_path)
            self.click_agree_button(page_pb)
            return page_pb
        except Exception as e:
            logging.error(f"Failed to upload for job check: {e}")

    def join_talent_community(self, in_page: Page = None):
        """
        This contains all the code to join the talent community.
        Args:
            in_page:

        Returns:

        """

        def create_talent_community_page(page: Page):
            """
            This method creates a new tab and navigates to the talent community page.
            Args:
                page:

            Returns:

            """
            try:
                page = self.create_new_tab(page.url)
                join_tn_link = page.query_selector('a[data-test-id="join-tn-link"]')

                if join_tn_link:
                    join_tn_link.click()
                    logging.info("Navigated to 'Join Talent Network'")
                else:
                    logging.error("Link not found")
                return page

            except Exception as e:
                logging.error(f"An error occurred: {e}")

        try:

            scat = self.safe_click_and_type
            email = self.rv.email
            qth = self.rv.location
            curr_company = self.rv.current_company
            curr_title = self.rv.current_title

            # Get talent window.
            talent_page = create_talent_community_page(in_page)
            talent_page.get_by_placeholder("Email").click()
            talent_page.get_by_placeholder("Email").fill("")
            scat(locator=talent_page.get_by_placeholder("Email"), input_message=email)
            scat(locator=talent_page.get_by_placeholder("Current Location"), input_message=qth)
            scat(locator=talent_page.get_by_placeholder("Current Company"), input_message=curr_company)
            scat(locator=talent_page.get_by_placeholder("Current Title"), input_message=curr_title)
            npc = talent_page.locator('i[data-test-id="careers-talent-network-privacy-checkbox-0"]')
            scat(locator=npc)
            sub_locator = talent_page.locator('button[data-test-id="jtn-submit-btn"]')
            scat(locator=sub_locator)
            logging.info("Submitted to talent. ")
        except Exception as e:
            logging.error(f"Failed to join the talent community: {e}")


def bimbo_reader_uploader(testmode: bool = False):
    logging.basicConfig(level=logging.INFO)
    with BimboJobSearcher() as bjs:
        job_check_page = bjs.upload_for_job_check()
        jtc = input("Join the talent community y/n")
        if jtc.strip().lower() == 'y':
            bjs.join_talent_community(in_page=job_check_page)
        bjs.close_with_test(testmode=testmode)


if __name__ == "__main__":
    bimbo_reader_uploader(testmode=False)
