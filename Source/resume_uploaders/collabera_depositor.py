from Data.reference_values import actual_values
from readers import GeneralReaderPlaywright
from readers.collabera_playwright import COLLABERA_URL

COLLABERA_TIMEOUT = 1000


def handle_file_chooser(file_chooser):
    # Select the resume file
    file_chooser.set_files(['path/to/your/resume.pdf'])

    # Close the file chooser
    file_chooser.dismiss()


class CollaberaDepositor(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=COLLABERA_URL, testmode=testmode)
        self.rv = actual_values

    def open_location_url(self):
        # open new tab and go to resume work.
        page_cc = self.create_new_tab()
        self.safe_click(page_cc.get_by_role("button", name="Accept"), timeout=COLLABERA_TIMEOUT)

        self.safe_click(page_cc.get_by_role("link", name="Submit Resume").click())

        # Fill in resume fields.
        self.click_type(page_cc.get_by_placeholder("First Name *"), self.rv.first_name, timeout=COLLABERA_TIMEOUT,
                        sleep_time=1)
        self.click_type(page_cc.get_by_placeholder("Last Name *"), self.rv.last_name, timeout=COLLABERA_TIMEOUT,
                        sleep_time=0)
        self.click_type(page_cc.get_by_placeholder("Email *"), self.rv.email, timeout=COLLABERA_TIMEOUT, sleep_time=1)
        self.click_type(page_cc.get_by_placeholder("Phone number *"), self.rv.phone, timeout=COLLABERA_TIMEOUT,
                        sleep_time=0)
        self.click_type(page_cc.get_by_placeholder("Linkedln Profile"), self.rv.linkedin_url, timeout=COLLABERA_TIMEOUT,
                        sleep_time=0)

        page_cc.get_by_label("Yes, I agree to the  Terms of Service  and Privacy Policy.").check()

        # Selector for the hidden file input element
        file_input_selector = '.wpcf7-form-control.wpcf7-drag-n-drop-file.d-none[type="file"]'

        # Wait for the file input to be present in the DOM (it might be hidden)
        page_cc.wait_for_selector(file_input_selector, state='attached')

        # Set the file on the input
        page_cc.set_input_files(file_input_selector, self.rv.current_resume_path)
        input("Don't forget to hit captcha and submit!")


with CollaberaDepositor() as cd:
    cd.open_location_url()
