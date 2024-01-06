import logging

from playwright.sync_api import Page

from Source import WorkdayReader
from Source.database_code.company_data_table_reader import company_data_table


class CubesmartMatcher(WorkdayReader):
    # Constants for websites to use. These are the same for all instances of this class.
    company = "cube_smart"

    cubesmart_personalization_url = company_data_table[company]["url"]

    def __init__(self, testmode: bool = False, customer_id: str = None):
        super().__init__(workday_url=self.cubesmart_personalization_url, testmode=testmode, customer_id=customer_id)
        self.cookies_accepted = False
        self.cubesmart_match()

    def cubesmart_match(self):
        cs_page = self.create_new_tab(website=self.cubesmart_personalization_url)
        self.accept_cookies(cs_page)

        start_here_button = cs_page.get_by_role(role="button", name="Start Here")
        self.safe_click(start_here_button)
        cs_page.set_input_files(selector='input[type="file"]', files=self.customer_data.current_resume_path)

        # Target the input field using its ID for reliable targeting
        location_input = cs_page.locator("#mat-input-0")
        self.safe_click_and_type(location_input, input_message=self.customer_data.location)
        # Target the dropdown menu container (replace with the actual container selector if needed)
        dropdown_menu = cs_page.locator(".mat-autocomplete-panel")  # Adjust selector as needed

        # Wait for the dropdown menu to be visible and populated
        dropdown_menu.wait_for(state="visible")
        option_count = dropdown_menu.locator(".mat-option").count()
        if option_count > 0:  # Use a comparison operator to check the count
            desired_option = dropdown_menu.locator(
                    f".mat-option:has-text('{self.customer_data.location}')")  # Replace with desired text
            self.safe_click(desired_option)
            cs_page.get_by_role(role="button", name="Get Jobs").click()
        else:
            # Handle the case where options are not present
            print("No options found in the dropdown menu.")
        # Target the option matching the entered text

        return cs_page

    def accept_cookies(self, in_page: Page):
        """
        Args:
            in_page:

        Returns:

        """
        logging.info("Start Accept cookies")
        if self.cookies_accepted:
            return
        # Accept cookies
        # Selector for the button. Using ID is usually the most reliable method.
        # Target the button using its ID, which is the most reliable locator
        accept_cookies_button = in_page.locator("#cookie-consent-accept-button")

        # Click the button
        try:
            self.safe_click(accept_cookies_button)
            self.cookies_accepted = True
        except TimeoutError:
            logging.info("Accept cookies button not found")
            self.cookies_accepted = False
        logging.info("End of Accept cookies")


if __name__ == '__main__':
    nic_ = "nic@secretsmokestack.com"
    csm = CubesmartMatcher(customer_id=nic_)
    print("finished")
