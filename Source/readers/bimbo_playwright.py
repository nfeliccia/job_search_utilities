from typing import Iterable, Any

from Data.reference_values import universal_search_terms
from readers_common import GeneralReaderPlaywright

# generate the parameters and teh base URL.
BIMBO_URL = "https://careers.bimbobakeriesusa.com/en-US/search"
BIMBO_PARAMETERS = parameters = [{"Keywords": x} for x in universal_search_terms]


class BimboReader(GeneralReaderPlaywright):  #

    def __init__(self, base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):

        """Initialize the BimboReader instance.

        Args:
        - base_url (str, optional): The base URL to start the scraping. Defaults to BIMBO_URL.
        - parameters (Iterable[dict], optional): A list of dictionaries containing search parameters.
                                                Defaults to BIMBO_PARAMETERS.
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """
        super().__init__()

        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = BIMBO_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = BIMBO_PARAMETERS

    def open_job_pages(self, base_url: str, parameters: Iterable[dict]) -> Any | None:
        """Open job pages using the provided base URL and search parameters.

        Args:
        - base_url (str): The base URL to start the search.
        - parameters (Iterable[dict]): A list of dictionaries containing search parameters.

        Returns:
        - object: The last opened page object for further operations.
        """

        # Open the base_url and search for each keyword in parameters
        if not parameters:
            print("No parameters provided. Exiting.")
            return None

        for param in parameters:
            ojp_age = self.create_new_tab(website=base_url)
            keyword = param.get("Keywords", "")  # Extract the keyword and remove quotes
            print(f"Searching for jobs with keyword: {keyword}")

            # Locate the input box labeled "Keyword:" and fill it with the keyword
            ojp_age.get_by_label("Keyword:").click()
            ojp_age.get_by_label("Keyword:").fill(keyword)
            ojp_age.get_by_role("link", name="Search").click()

        # Return the ojp_age for further operations if needed (this will be the last opened ojp_age)
        return ojp_age

    def close_with_test(self, testmode: bool = False) -> None:
        """Close the browser session. Behavior varies based on the test mode.

        Args:
        - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
        """

        if testmode:
            print("Browser session closed in test mode.")
        else:
            input("Press Enter to close the browser session.")


def bimbo_reader(base_url: str = None, parameters: Iterable[dict] = None, testmode: bool = False):
    """A wrapper function for the BimboReader class.

    Args:
    - base_url (str, optional): The base URL to start the scraping. Defaults to BIMBO_URL.
    - parameters (Iterable[dict], optional): A list of dictionaries containing search parameters.
                                            Defaults to BIMBO_PARAMETERS.
    - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
    """

    with BimboReader(base_url=base_url, parameters=parameters, testmode=testmode) as br:
        page = br.open_job_pages(base_url=br.base_url, parameters=br.parameters)
        br.close_with_test(testmode=br.testmode)
        return page


if __name__ == "__main__":
    bimbo_reader(base_url=BIMBO_URL, parameters=BIMBO_PARAMETERS, testmode=False)
