from Data.reference_values import universal_search_terms
from readers import GeneralReaderPlaywright

# generate the parameters and teh base URL.
BIMBO_URL = "https://careers.bimbobakeriesusa.com/en-US/search"


class BimboReader(GeneralReaderPlaywright):  #

    def __init__(self, testmode: bool = False):
        super().__init__(root_website=BIMBO_URL, testmode=testmode)

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


def bimbo_reader(testmode: bool = False):
    """A wrapper function for the BimboReader class.

    Args:
    - base_url (str, optional): The base URL to start the scraping. Defaults to BIMBO_URL.
    - parameters (Iterable[dict], optional): A list of dictionaries containing search parameters.
                                            Defaults to BIMBO_PARAMETERS.
    - testmode (bool, optional): A flag indicating if the instance is in test mode. Defaults to False.
    """

    with BimboReader(testmode=testmode) as br:
        pages_list = []
        for term in universal_search_terms:
            pages_list.append(br.search_keyword(keyword=term))
        br.close_with_test(testmode=br.testmode)
        return pages_list


if __name__ == "__main__":
    bimbo_reader(testmode=False)
