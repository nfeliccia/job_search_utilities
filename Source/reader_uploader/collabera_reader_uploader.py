import logging

from Source import GeneralReaderPlaywright
from Source.database_code.company_data_table_reader import company_data_table


class CollaberaReader(GeneralReaderPlaywright):
    company_name = "collabera"
    COLLABERA_URL = company_data_table[company_name]["url"]
    resume_upload = company_data_table[company_name]["upload_resume"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(root_website=self.COLLABERA_URL, testmode=testmode, customer_id=customer_id)

    def run_collabera(self):
        self.search_multiple_keywords()
        self.close_with_test(testmode=self.testmode)

    def accept_cookies(self, page=None):
        if page is None:
            logging.error("Page cannot be None.")
            return

        accept_button = page.locator("#wt-cli-accept-all-btn")
        if accept_button.is_visible():
            element = accept_button.element_handle()
            element.wait_for_element_state("visible")
            self.safe_click(accept_button, timeout=1000, error_message="Error during click operation")

    def search_keyword(self, keyword: str) -> str:
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """
        if not keyword:
            logging.error("Keyword cannot be None or an empty string.")
            return ""
        page = self.create_new_tab()
        jt_or_k = page.get_by_placeholder("Job Title or Keywords")
        l_ = page.locator('input[name="location"]')
        self.click_type(locator=jt_or_k, input_message=keyword, enter=False)
        self.click_type(locator=l_, input_message=self.customer_data.location, enter=True)
        self.accept_cookies(page=page)
        sk_content = page.content()
        return sk_content

    def search_multiple_keywords(self):
        pages_list = []
        for keyword in self.customer_data.search_terms:
            pages_list.append(self.search_keyword(keyword))
        return pages_list

    def upload_resume(self, page=None):

        page_cc = self.create_new_tab(self.resume_upload)
        self.accept_cookies(page=page_cc)
        # Fill in resume fields.
        self.click_type(page_cc.get_by_placeholder("First Name *"), self.customer_data.first_name)
        self.click_type(page_cc.get_by_placeholder("Last Name *"), self.customer_data.last_name)
        self.click_type(page_cc.get_by_placeholder("Email *"), self.customer_data.email)
        self.click_type(page_cc.get_by_placeholder("Phone number *"), self.customer_data.phone)
        self.click_type(page_cc.get_by_placeholder("Linkedln Profile"), self.customer_data.linkedin_url)

        page_cc.get_by_label("Yes, I agree to the  Terms of Service  and Privacy Policy.").check()

        # Selector for the hidden file input element
        file_input_selector = '.wpcf7-form-control.wpcf7-drag-n-drop-file.d-none[type="file"]'

        # Wait for the file input to be present in the DOM (it might be hidden)
        page_cc.wait_for_selector(file_input_selector, state='attached')

        # Set the file on the input
        page_cc.set_input_files(file_input_selector, self.customer_data.current_resume_path)
        input("Don't forget to hit captcha and submit!")



if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    testmode_ = False
    cr = CollaberaReader(testmode=testmode_, customer_id=nic_)
    # cr.search_multiple_keywords()
    cr.upload_resume()
