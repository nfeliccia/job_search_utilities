import keyring

from Data.reference_values import actual_values, universal_search_terms
from Source import GeneralReaderPlaywright


class CyberCodersReader(GeneralReaderPlaywright):
    CYBERCODERS_URL = "https://www.cybercoders.com/"
    LOCATION = "Philadelphia, PA"

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=self.CYBERCODERS_URL, testmode=testmode)
        self.rv = actual_values

    def cyber_coders_login(self):
        username = actual_values.email
        secret_password = keyring.get_password(service_name=self.CYBERCODERS_URL, username=username)
        ccl_page = self.create_new_tab()
        ccl_page.locator("#dropdown-login").get_by_text("Login").click()
        ccl_page.get_by_placeholder("Email address").click()
        ccl_page.get_by_placeholder("Email address").fill(self.rv.email)
        ccl_page.get_by_placeholder("Password", exact=True).click()
        ccl_page.get_by_placeholder("Password", exact=True).fill(secret_password)
        ccl_page.get_by_role("button", name="Login").click()
        ccl_page.wait_for_load_state("networkidle")
        logged_in_url = ccl_page.url
        return logged_in_url

    def search_a_keyword(self, in_keyword: str, qth: str = None, in_url: str = None):
        if in_url is None:
            in_url = self.CYBERCODERS_URL
        page = self.create_new_tab(in_url)

        search_input = page.locator("#global-search-terms")
        self.safe_click_and_type(search_input, in_keyword)
        location_input = page.locator("#global-search-location")
        self.safe_click_and_type(location_input, qth)
        search_button_selector = page.locator("button.hidden-search-icon[type='submit']")
        self.safe_click(search_button_selector, timeout=5000)
        return page


with CyberCodersReader() as cr:
    logged_in_url = cr.cyber_coders_login()
    for keword in universal_search_terms:
        page = cr.search_a_keyword(in_keyword=keword, qth=cr.LOCATION, in_url=logged_in_url)
        page.wait_for_load_state("networkidle")
    cr.close_with_test(testmode=cr.testmode)
