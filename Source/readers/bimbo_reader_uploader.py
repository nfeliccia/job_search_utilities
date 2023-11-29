from time import sleep

from playwright.sync_api import Page

from Data.reference_values import actual_values
from common_code import GeneralReaderPlaywright


class BimboJobSearcher(GeneralReaderPlaywright):
    BIMBOURL = "https://careers.bimbobakeriesusa.com/careers"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.BIMBOURL, testmode=testmode)
        self.rv = actual_values

    def upload_for_job_check(self):
        """
        The first part here uploads the resume for the job check.
        Returns:
            Page object
        """

        page_pb = self.create_new_tab()
        selector = '.dropzone-container input[type="file"]'
        page_pb.wait_for_selector(selector, state="visible")

        # If the desired input is the first one, use first=0; if it's the second one, use first=1
        locator = page_pb.locator(selector).nth(0)
        locator.set_input_files(self.rv.current_resume_path)

        # Define the selector for the "I Agree" button
        button_selector = 'button[data-test-id="confirm-upload-resume"]'
        page_pb.wait_for_selector(button_selector, state="visible")
        page_pb.click(button_selector)

        return page_pb

    def join_talent_community(self, in_page: Page = None):
        in_page.get_by_role("button", name="join the talent community").click()
        sleep(4 * self.sleep_time)

        in_page.get_by_placeholder("Email").click()
        # Wait for the Email input field to appear
        in_page.wait_for_selector('input[placeholder="Email"]', state="visible")
        self.click_type(in_page.get_by_placeholder("Email"), input_message=self.rv.email)

        cl_ = in_page.get_by_placeholder("Current Location")
        cc_ = in_page.get_by_placeholder("Current Company")
        ct_ = in_page.get_by_placeholder("Current Title")

        self.click_type(cl_, input_message=self.rv.location)
        self.click_type(cc_, input_message=self.rv.current_company)
        self.click_type(ct_, input_message=self.rv.current_title)

        in_page.locator("[data-test-id=\"careers-talent-network-privacy-checkbox-0\"]").click()
        in_page.locator("[data-test-id=\"jtn-submit-btn\"]").click()


def bimbo_reader_uplaoder(testmode: bool = False):
    with BimboJobSearcher() as bjs:
        bjs.upload_for_job_check()
        jtc = input("Join the talent community y/n")
        if jtc.lower() == "y":
            bjs.join_talent_community()
        bjs.close_with_test(testmode=testmode)


if __name__ == "__main__":
    bimbo_reader_uplaoder(testmode=False)
