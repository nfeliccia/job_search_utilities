from time import sleep

from Data.reference_values import actual_values
from readers import GeneralReaderPlaywright

BIMBOURL = "https://careers.bimbobakeriesusa.com/careers"


class BimboJobSearcher(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=BIMBOURL, testmode=testmode)
        self.rv = actual_values

    def process_bimbo(self):
        page_pb = self.create_new_tab()
        selector = '.dropzone-container input[type="file"]'
        page_pb.wait_for_selector(selector, state="visible")
        # If the desired input is the first one, use first=0; if it's the second one, use first=1
        locator = page_pb.locator(selector).nth(0)  # Replace 0 with 1 if the desired input is the second one
        locator.set_input_files(self.rv.current_resume_path)
        sleep(1)
        # Define the selector for the "I Agree" button
        button_selector = 'button[data-test-id="confirm-upload-resume"]'
        page_pb.wait_for_selector(button_selector, state="visible")
        page_pb.click(button_selector)
        # Wait for the button to be visible and clickable
        # Wait for the "join the talent community" button to appear
        page_pb.get_by_role("button", name="join the talent community").click()
        sleep(8)

        page_pb.get_by_placeholder("Email").click()
        # Wait for the Email input field to appear
        page_pb.wait_for_selector('input[placeholder="Email"]', state="visible")
        self.click_type(page_pb.get_by_placeholder("Email"), input_message=self.rv.email, sleep_time=1)

        cl_ = page_pb.get_by_placeholder("Current Location")
        cc_ = page_pb.get_by_placeholder("Current Company")
        ct_ = page_pb.get_by_placeholder("Current Title")

        self.click_type(cl_, input_message=self.rv.location, sleep_time=1)
        self.click_type(cc_, input_message=self.rv.current_company, sleep_time=1)
        self.click_type(ct_, input_message=self.rv.current_title, sleep_time=1)

        page_pb.locator("[data-test-id=\"careers-talent-network-privacy-checkbox-0\"]").click()
        page_pb.locator("[data-test-id=\"jtn-submit-btn\"]").click()


with BimboJobSearcher() as bjs:
    bjs.process_bimbo()
    bjs.close_with_test(testmode=False)
