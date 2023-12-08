from time import sleep

from Data.reference_values import actual_values
from common_code import GeneralReaderPlaywright

rv = actual_values


class WellsFargoDepositor(GeneralReaderPlaywright):
    wells_fargo_url = "https://www.wellsfargojobs.com/"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.wells_fargo_url, testmode=testmode)

    def submit_resume(self):
        page_sr = self.create_new_tab()
        self.safe_click(page_sr.get_by_role("button", name="Accept All"))
        self.safe_click(page_sr.get_by_role("link", name="Join our Talent Community"))

        with page_sr.expect_popup() as popup_info:
            # Adopt the new page from the value of the popup.
            page_form = popup_info.value
            self.click_type(page_form.get_by_label("Full Name*"), input_message=rv.first_name + " " + rv.last_name)
            self.click_type(page_form.get_by_label("Email Address*"), input_message=rv.email)
            self.click_type(page_form.get_by_label("Phone number"), input_message=rv.phone)

            perf_loc = page_form.locator(".css-19bb58m")
            self.click_type(perf_loc, input_message="Philadelphia, ")
            page_form.get_by_label("Preferred location(s)").fill("Philadelphia, ")
            page_form.get_by_text("Philadelphia, Pennsylvania, United States of America", exact=True).click()

            status_ = "Career Status*"
            page_form.get_by_label(status_).click()
            page_form.get_by_role("option", name="Experienced Professional").click()
            page_form.get_by_label(status_).click()
            page_form.get_by_label(status_).press("Enter")

            self.safe_click(page_form.get_by_label("Highest Degree Level*"))
            page_form.get_by_label("Highest Degree Level*").press("Enter")
            sleep(1)
            page_form.get_by_text("Masters Completed").click()
            sleep(1)
            page_form.get_by_label("Military Status*").click()
            sleep(1)
            page_form.get_by_text("Not Applicable").click()
            page_form.locator("i").click()

            file_input_selector = 'input[data-automation="file-uploader-control/input"]'
            file_path = rv.current_resume_path  # Replace with the actual path to your resume file

            page_form.set_input_files(file_input_selector, file_path)
            page_form.get_by_role("button", name="Submit").click()

            print("done")


with WellsFargoDepositor(testmode=False) as wf_reader:
    wf_reader.submit_resume()
    wf_reader.close_with_test(testmode=False)
