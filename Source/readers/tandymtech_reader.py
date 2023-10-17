from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from readers import GeneralReader

"""
10/17/2023 - Still needs some work. 
"""


def build_tandym_tech_urls(keyword: str, where: str) -> str:
    """
    Builds a URL for the Tandym Tech job search results page.

    Args:
        keyword (str): The keyword to search for.
        where (str): The location to search in.

    Returns:
        str: The URL for the Tandym Tech job search results page.
    """

    base_url = "https://tandymtech.com/job-seekers/tech-search-results/"
    query_params = {
        "keyword": keyword,
        "where": where,
    }

    return GeneralReader().construct_url(base_url=base_url, query_params=query_params)


def click_cookies_button(reader: GeneralReader, url: str) -> None:
    """
    Clicks the cookies button on the specified URL.

    Args:
        reader (GeneralReader): The GeneralReader instance.
        url (str): The URL to click the cookies button on.
    """

    try:
        cookies_button = reader.webdriver.find_element_by_css_selector(".hs-eu-confirmation-button")
        cookies_button.click()
    except Exception:
        print(f"Error clicking cookies button on {url}")


def scroll_to_bottom_of_section_and_click_load_more(reader: GeneralReader, url: str) -> None:
    """
    Scrolls to the bottom of the section and clicks the 'Load more' button on the specified URL.

    Args:
        reader (GeneralReader): The GeneralReader instance.
        url (str): The URL to scroll to the bottom of and click the 'Load more' button on.
    """

    reader.webdriver.get(url)
    sleep(3)
    try:
        reader.webdriver.find_element(by=By.CSS_SELECTOR, value=".cards").execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight;")
        reader.webdriver.find_element_by_xpath("//*[contains(text(), 'Load more')]").click()
    except NoSuchElementException:
        print(f"Error scrolling to bottom of section and clicking 'Load more' button on {url}")


def tandym_tech_reader(testmode=False) -> None:
    """

    This script automates the process of navigating to two specific URLs using Selenium.
    For each URL, the script performs the following actions:
    1. Opens the URL in a Chrome browser.
    2. Clicks the cookies button.
    3. Waits for and clicks on the 'hs-eu-confirmation-button'.
    4. For the second URL, checks a specific checkbox if it's not already checked.
    5. Scrolls to the bottom of the section and clicks the 'Load more' button.
    6. Waits for the user to press Enter and then quits the browser.


    Args:
        testmode: RUn in test mode.

    Returns:

    """

    reader = GeneralReader()

    # Build the URLs for the job postings.
    pennsylvania_url = build_tandym_tech_urls(keyword="", where="19124,%20Philadelphia,%20Pennsylvania")
    remote_url = build_tandym_tech_urls(keyword="Remote", where="")

    # Open the web pages in new tabs and click the cookies button.
    reader.webdriver.execute_script(f"window.open('{pennsylvania_url}', '_blank');")
    click_cookies_button(reader, pennsylvania_url)
    reader.webdriver.execute_script(f"window.open('{remote_url}', '_blank');")
    click_cookies_button(reader, remote_url)

    # Scroll to the bottom of the section and click the 'Load more' button.
    scroll_to_bottom_of_section_and_click_load_more(reader, pennsylvania_url)
    scroll_to_bottom_of_section_and_click_load_more(reader, remote_url)

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    tandym_tech_reader()
