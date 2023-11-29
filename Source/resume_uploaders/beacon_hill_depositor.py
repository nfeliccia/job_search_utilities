from time import sleep

from Data.reference_values import actual_values
from common_code import GeneralReaderPlaywright

rv = actual_values


class BeaconHillUploader(GeneralReaderPlaywright):
    beacon_hill_url = "https://jobs.beaconhillstaffing.com/submit-resume/"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.beacon_hill_url, testmode=testmode)

    def submit_resume(self):
        # Since the base URL already contains the location, we can just use the create_new_tab method without arguments.
        page_sr = self.create_new_tab()
        self.safe_click(page_sr.get_by_role("link", name="Later"), timeout=5000)

        # Fill in the name fields.
        # //*[@id="input_3_2"]
        self.click_type(locator=page_sr.locator("xpath=//*[@id='input_3_1_3']"), input_message=rv.first_name)
        self.click_type(locator=page_sr.locator("xpath=//*[@id='input_3_1_6']"), input_message=rv.last_name)
        self.click_type(locator=page_sr.locator("xpath=//*[@id='input_3_2']"), input_message=rv.email)
        self.click_type(locator=page_sr.locator("xpath=//*[@id='input_3_3']"), input_message=rv.phone)

        page_sr.get_by_label("In what field is your primary").select_option("Technology")
        page_sr.locator("#input_3_15").select_option("Philadelphia, PA (Temp and Perm)")

        page_sr.set_input_files('input[name="input_4"]', rv.current_resume_path)
        page_sr.click("#gform_submit_button_3")

        sleep(5)


with BeaconHillUploader(testmode=False) as bhu_reader:
    bhu_reader.submit_resume()
    bhu_reader.close_with_test(testmode=False)
