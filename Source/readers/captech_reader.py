from typing import Iterable

from readers import GeneralReader


def captech_executer(parameters: Iterable[dict] = None, testmode=False):
    """
    Opens the CapTech Consulting job openings page for Philadelphia in new tabs.

    Args:
        parameters (Iterable[dict], optional): A list of dictionaries containing the query parameters for the job openings pages. Defaults to None.
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    # Create a GeneralReader object.
    reader = GeneralReader()

    # Set the base URL.
    base_url = "https://www.captechconsulting.com/careers/current-openings/"

    # Construct the URLs for the job openings pages.
    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    # Open the web pages in new tabs.
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        reader.webdriver.execute_script(window_open_script)

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


def captech_reader(testmode=False):
    """
    Opens the CapTech Consulting job openings page for Philadelphia and the job openings pages for Machine Learning, Data Science, and Python in new tabs.

    Args:
        testmode (bool, optional): Whether the test mode is enabled. Defaults to False.

    Returns:
        None
    """

    parameters = [{"keywords": "", "location": "253788", "page": "1", },
                  {"keywords": "Machine Learning", "page": "1", },
                  {"keywords": "Data Science", "page": "1", },
                  {"keywords": "Python", "page": "1", }]

    captech_executer(parameters, testmode=testmode)


# Uncomment the below line when you want to execute the script

if __name__ == "__main__":
    captech_reader(testmode=False)
