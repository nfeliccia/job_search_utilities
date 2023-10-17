import typing

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readers import GeneralReader


def collabera_executer(parameters: typing.Iterable[dict] = None, testmode=False):
    """
    Opens the Collabera job search page for the specified parameters in new tabs.

    Args:
        parameters (Iterable[dict], optional): A list of dictionaries containing the query parameters for the job search page. Defaults to None.
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    # Create a GeneralReader object.
    reader = GeneralReader()

    # Set the base URL.
    base_url = "https://collabera.com/job-search/"

    # Construct the URLs for the job search pages.
    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    # Open the web pages in new tabs.
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        reader.webdriver.execute_script(window_open_script)

        # Wait for the page to load.
        WebDriverWait(reader.webdriver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "header.header a.navbar-brand")))

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


def collabera_reader(testmode=False):
    """
    Opens the Collabera job search page for the specified parameters in new tabs.

    Args:
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    parameters = [
        {"sort_by": "dateposted", "industry": "", "keyword": "Python", "Posteddays": "0"},
        {"sort_by": "dateposted", "industry": "", "keyword": "Data+Science", "Posteddays": "0"},
        {"sort_by": "dateposted", "industry": "", "keyword": "Machine+Learning", "Posteddays": "0"}]

    collabera_executer(parameters, testmode=testmode)


if __name__ == '__main__':
    collabera_reader(testmode=False)
