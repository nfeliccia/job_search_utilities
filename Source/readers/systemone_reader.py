from typing import Iterable

from readers import initialize_webdriver
from readers.readers_common import construct_url, close_with_test


def systemone_executer(parameters: Iterable[dict] = None, testmode=False):
    # Initialize the web driver
    driver = initialize_webdriver()

    # Set base URL and static path/hash components
    base_url = "https://jobs.systemone.com/"
    path = "l/recruiting/jobsearchaction/b440eda6-9cc2-11e4-a7c5-bc764e10782d"
    static_hash = "f40610d2-abe2-11ed-9711-42010a8a0fd9"  # This is the static hash we're reusing
    full_base_url = f"{base_url}{path}/{static_hash}/false"

    # Construct the search URLs
    urls = [construct_url(base_url=full_base_url, query_params=x) for x in parameters]
    for url in urls:
        # Open a new tab
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        driver.execute_script(window_open_script)

    # Handle cleanup
    close_with_test(driver=driver, testmode=testmode)


def systemone_reader(testmode=False):
    parameters = [
        {"sortBy": "beginTime", "term": '"Data Scientist"', "title": "", "postalCode": ""},
        {"sortBy": "beginTime", "term": '"Machine Learning"', "title": "", "postalCode": ""}
    ]
    systemone_executer(parameters=parameters, testmode=testmode)


# Test the script
if __name__ == "__main__":
    systemone_reader(testmode=False)
