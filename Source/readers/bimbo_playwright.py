from Data.reference_values import universal_search_terms
from readers_common import GeneralReaderPlaywright

# generate the parameters and teh base URL.
BIMBO_URL = "https://careers.bimbobakeriesusa.com/en-US/search"


def safe_click(locator, timeout=1000, error_message="Error during click operation"):
    """Attempt to click a locator with error handling and custom timeout."""
    try:
        locator.click(timeout=timeout)
    except Exception as e:
        print(f"{error_message}: {e}")

class BimboReader(GeneralReaderPlaywright):  #

    def __init__(self, base_url: str = None, testmode: bool = False):

        """Initialize the BimboReader instance.

        Args:
        - base_url (str, optional): The base URL to start the scraping. Defaults to BIMBO_URL.
        - parameters (Iterable[dict], optional): A list of dictionaries containing search parameters.
                                                Defaults to BIMBO_PARAMETERS.
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """
        super().__init__(root_website=base_url, testmode=testmode)

    def search_keyword(self, keyword: str) -> str:
        """
        The purpose of this code is to search an individual keyword. It will open a new tab and search for the keyword.
        Args:
          keyword: a word to search for.
          qth: location


        Returns:
          string. HTML of the page.

        """
        ojp_age = self.create_new_tab()
        l_ = "Keyword:"
        ojp_age.get_by_label(l_).click()
        ojp_age.get_by_label(l_).fill(keyword)
        ojp_age.get_by_role("link", name="Search").click()
        return ojp_age.content()


    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


def bimbo_reader(base_url: str = None, testmode: bool = False):
    """A wrapper function for the BimboReader class.

    Args:
    - base_url (str, optional): The base URL to start the scraping. Defaults to BIMBO_URL.
    - parameters (Iterable[dict], optional): A list of dictionaries containing search parameters.
                                            Defaults to BIMBO_PARAMETERS.
    - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
    """

    with BimboReader(base_url=base_url, testmode=testmode) as br:
        pages_list = [br.search_keyword(keyword=term) for term in universal_search_terms]
        br.close_with_test(testmode=br.testmode)
        return pages_list


if __name__ == "__main__":
    bimbo_reader(base_url=BIMBO_URL, testmode=False)
