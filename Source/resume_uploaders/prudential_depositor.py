from Data.reference_values import actual_values
from common_code import GeneralReaderPlaywright

rv = actual_values


class PrudentialDepositor(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website="https://jobs.prudential.com/us-en", testmode=testmode)

    def fill_out_form(self, page):
        self.perform_initial_clicks(page)
        self.fill_form_fields(page)
        self.upload_resume_file(page)
        self.finalize_form_submission(page)

    def perform_initial_clicks(self, page):
        self.safe_click(page.get_by_role("button", name="Close"))
        self.safe_click(page.get_by_role("link", name="Learn More"))
        self.safe_click(page.get_by_role("button", name="Get Started Join the Talent"))

    def fill_form_fields(self, page):
        self.click_type(page.get_by_label("First Name\n *Required Field"), input_message=rv.first_name)
        self.click_type(page.get_by_label("Last Name\n *Required Field"), input_message=rv.last_name)
        self.click_type(page.get_by_label("Email Address\n *Required Field"), input_message=rv.email)
        self.click_type(page.get_by_label("LinkedIn Profile URL"), input_message=rv.linkedin_url)

    def upload_resume_file(self, page):
        with page.expect_file_chooser() as file_chooser_info:
            page.click('input[type="file"]')  # Replace with the appropriate selector
        file_chooser = file_chooser_info.value
        file_chooser.set_files(rv.current_resume_path)  # Replace with the path to your resume
        page.wait_for_load_state()

    def finalize_form_submission(self, page):
        self.safe_click(page.get_by_text("Yes, I have read, understand"))
        self.safe_click(page.get_by_role("button", name="Join The Network"))


with PrudentialDepositor(testmode=False) as prudential_reader:
    prudential_reader.fill_out_form(page=prudential_reader.create_new_tab())
    prudential_reader.close_with_test(testmode=False)
