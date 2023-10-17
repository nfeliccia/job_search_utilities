from typing import Iterable

from readers import GeneralReader


def jacobs_executer(parameters: Iterable[dict] = None, testmode=False):
    """
    Opens the Jacobs job search results page for the specified parameters in new tabs.

    Args:
        parameters (Iterable[dict], optional): A list of dictionaries containing the query parameters for the job search results page. Defaults to None.
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    # Create a GeneralReader object.
    reader = GeneralReader()

    # Set the base URL.
    base_url = "https://careers.jacobs.com/job-search-results/"

    # Construct the URLs for the job search results pages.
    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    # Open the web pages in new tabs.
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        reader.webdriver.execute_script(window_open_script)

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


def jacobs_reader(testmode=False):
    """
    Opens the Jacobs job search results page for the specified parameters in new tabs.

    Args:
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
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
