from typing import Iterable

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readers import GeneralReader


def susquehanna_executer(parameters: Iterable[dict] = None, testmode=False):
    """
    Opens the Susquehanna International Group careers page in new tabs for the specified keywords.

    Args:
        parameters (Iterable[dict], optional): A list of dictionaries containing the query parameters for the careers pages. Defaults to None.
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    # Create a GeneralReader object.
    reader = GeneralReader()

    # Base URL for Susquehanna International Group careers page.
    base_url = "https://careers.sig.com/search-results"

    # Construct the search URLs.
    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    # Open the web pages in new tabs.
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        reader.webdriver.execute_script(window_open_script)

        # Wait for the page to load and check for the "Allow" button in the cookie popup, then click it.
        try:
            #
            element_xpath = '/html/body/div[1]/section[1]/div/div/div/div[2]/button'
            locator = (By.XPATH, element_xpath)
            element_located = EC.presence_of_element_located(locator=locator)
            allow_button = WebDriverWait(reader.webdriver, 2).until(element_located)
            allow_button.click()

        except (NoSuchElementException, TimeoutException) as _:
            print("Cookie consent popup not found or handled for tab with keyword:  ")

        try:
            # Add an explicit wait for the checkbox element to be visible
            child__checkbox = '//*[@id="JobLocationBody"]/div[1]/div/div[2]/ul/li[1]/label/span[1]'
            checkbox_element_locator = (By.XPATH, child__checkbox)
            located = EC.visibility_of_element_located(checkbox_element_locator)
            checkbox = WebDriverWait(reader.webdriver, timeout=4).until(located)
            checkbox.click()
        except (NoSuchElementException, TimeoutException) as _:
            print("Checkbox not found in tab with keyword:  ")

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


def susquehanna_reader(testmode=False):
    """
    Opens the Susquehanna International Group careers page in new tabs for the specified keywords.

    Args:
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    parameters = [
        {"keywords": '"Data Science"'},
        {"keywords": '"Machine Learning"'},
        {"keywords": '"Python"'}
    ]

    susquehanna_executer(parameters=parameters, testmode=testmode)


# Test the script
if __name__ == "__main__":
    susquehanna_reader(testmode=False)
