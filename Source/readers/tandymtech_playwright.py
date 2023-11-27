from readers_common_old import GeneralReaderPlaywright

from Data.reference_values import universal_search_terms


def safe_click(locator, timeout=1000, error_message="Error during click operation"):
    """Attempt to click a locator with error handling and custom timeout."""
    try:
        locator.click(timeout=timeout)
    except Exception as e:
        print(f"{error_message}: {e}")


class TandymTechReader(GeneralReaderPlaywright):

    def __init__(self, testmode: bool = False):
        super().__init__(root_website="https://tandymtech.com/job-seekers", testmode=testmode)

    def search_keyword(self, keyword: str, qth: str = None):
        page = self.create_new_tab()
        safe_click(page.get_by_role("button", name="Accept"))

        # Filling in the keyword search
        job_id = "Job title, keyword, or job ID"
        code = "City, state or ZIP code"

        page.get_by_placeholder(job_id).click()
        page.get_by_placeholder(job_id).fill(keyword)
        e_ = "Enter"
        page.get_by_placeholder(job_id).press(e_)

        # Location search
        page.get_by_placeholder(code).click()
        page.get_by_placeholder(code).fill(qth)
        page.get_by_placeholder(code).press(e_)

        page.get_by_role("link", name="Start My Search").click()
        safe_click(page.frame_locator("#bullHornJobResult").get_by_role("button", name="Accept"))

    def open_all_keywords(self, keywords, qth: str = None):
        # Iterating through each term in the provided keywords list
        for keyword in keywords:
            self.search_keyword(keyword, qth=qth)

    def close_with_test(self, testmode: bool = False):
        """Close the browser session. Behavior varies based on the test mode."""
        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


if __name__ == "__main__":
    testmode = False
    with TandymTechReader() as reader:
        reader.open_all_keywords(keywords=universal_search_terms, qth="Philadelphia, PA")
        reader.close_with_test(testmode=False)
