from typing import Iterable

from readers import initialize_webdriver, construct_url
from readers.readers_common import close_with_test


def jacobs_executer(parameters: Iterable[dict] = None, testmode=False):
    """
    The purpose of this function is to open a new tab with the URl for each parameter in the list of parameters.
    Args:
        parameters:
        testmode:

    Returns:

    """

    # Initialize the webdriver (assuming Chrome, but can be changed)
    driver = initialize_webdriver()

    base_url = "https://careers.jacobs.com/job-search-results/"
    urls = [construct_url(base_url=base_url, query_params=x) for x in parameters]
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        driver.execute_script(window_open_script)

    close_with_test(driver=driver, testmode=testmode)


def jacobs_reader(testmode=False):
    """

    Args:
        testmode:Boolean to determine if the browser should be closed after the test is complete

    Returns:

    """
    job_titles = ["'Data Scientist Associate'", "'Data Scientist Lead'", "'Data Scientist'", "'Machine Learning'",
                  "'Python'"]
    parameters = [{
        'keyword': keyword, 'location': 'Philadelphia, PA, USA', 'latitude': '39.9525839', 'longitude': '-75.1652215',
        'radius': '50'
    } for keyword in job_titles]
    jacobs_executer(parameters=parameters, testmode=testmode)


if __name__ == "__main__":
    jacobs_reader(testmode=False)
