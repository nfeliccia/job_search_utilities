import typing

from readers import GeneralReader


def bimbo_reader(parameters: typing.Iterable[dict], testmode=False):
    """

    Args:
        parameters: parameters for the strings
        testmode: boolean to determine if the browser should be closed after the test is complete

    Returns:
        None

    """
    # Create a GeneralReader object.
    reader = GeneralReader()

    # Construct the URLs for the job postings.
    base_url = "https://careers.bimbobakeriesusa.com/en-US/search"
    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    # Open the web pages in new tabs.
    for url in urls:
        reader.webdriver.open_new_tab(url=url)

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


def bimbo_executer():
    parameters = [{"Keywords": '"Python"'}, {"Keywords": '"Data Science"'}, {"Keywords": '"Machine Learning"'}]
    bimbo_reader(parameters, testmode=False)


if __name__ == "__main__":
    bimbo_executer()
