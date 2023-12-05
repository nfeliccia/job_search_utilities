from Data.reference_values import actual_values
from Source import GeneralReaderPlaywright

"""

Note, some sort of security keeps it from going through when autofilled. 
"""

CUBESMART_URL = "https://careers.cubesmart.com/careers-home/jobs"


class CubeSmartTalentSumbitter(GeneralReaderPlaywright):
    def __init__(self, testmode: bool = False):
        super().__init__(root_website=CUBESMART_URL, testmode=testmode)
        self.rv = actual_values

    def fill_and_sumbit_form(self):
        page_cc = self.create_new_tab()

        # Accept cookies
        # Selector for the button. Using ID is usually the most reliable method.
        button_selector = '#cookie-consent-accept-button'
        page_cc.wait_for_selector(button_selector, state='visible')
        page_cc.click(button_selector)

        # Go to talent network page. This is the page where the form is located.
        page_cc.locator("header").get_by_role("link", name="Join Our Talent Network").click()
        self.click_type(page_cc.get_by_label("First Name*"), input_message=self.rv.first_name)
        self.click_type(page_cc.get_by_label("Last Name*"), input_message=self.rv.last_name)
        self.click_type(page_cc.get_by_label("Email*"), input_message=self.rv.email)
        self.click_type(page_cc.get_by_label("Address 1"), input_message=self.rv.address)
        self.click_type(page_cc.get_by_label("City"), input_message=self.rv.city)
        self.click_type(page_cc.get_by_label("State"), input_message=self.rv.state)
        self.click_type(page_cc.get_by_label("Zip"), input_message=self.rv.zip)
        country_path = "suf-dropdown > .mat-form-field > .mat-form-field-wrapper > .mat-form-field-flex > .mat-form-field-infix"
        page_cc.locator(country_path).first.click()
        page_cc.get_by_text("United States", exact=True).click()
        self.click_type(page_cc.get_by_label("Phone Number*"), input_message=self.rv.phone)
        self.safe_click(page_cc.get_by_label("Phone Type*").locator("span"))
        page_cc.get_by_text("Mobile").click()
        page_cc.get_by_label("Best Communication Method").locator("span").click()
        page_cc.get_by_text("Phone", exact=True).click()
        page_cc.get_by_label("Best Time to Contact").locator("span").click()
        page_cc.get_by_text("Morning").click()
        page_cc.locator(".mat-checkbox-inner-container").click()
        # Selector for the button. Adjust if needed.
        button_selector = '.mat-flat-button.mat-primary'

        # Wait for the button to be visible and click it
        page_cc.wait_for_selector(button_selector)

        page_cc.click(button_selector)


with CubeSmartTalentSumbitter() as cst:
    cst.fill_and_sumbit_form()
    cst.close_with_test(testmode=False)
