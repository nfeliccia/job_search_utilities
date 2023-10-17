import typing

from readers import GeneralReader


def tech_in_motion_executer(base_url: str, parameters: typing.Iterable[dict], testmode=False):
    """
    Opens the web pages for the given job postings.

    Args:
        base_url: The base URL for the job postings.
        parameters: A list of dictionaries containing the query parameters for each job posting.
        testmode: Whether to operate in test mode and close the browser window automatically.

    Returns:
        None
    """

    reader = GeneralReader()

    urls = [reader.construct_url(base_url=base_url, query_params=x) for x in parameters]

    for url in urls:
        reader.open_a_tab(url)

    reader.close_with_test(testmode)


def tech_in_motion_reader(testmode=False):
    base_url = "https://motionrecruitment.com/tech-jobs"
    parameters = [
        {"radius": "25", "search-city": "19124", "postalcode": "19124", "remote": "true", "keywords": keyword}
        for keyword in ["Machine+Learning", "Data+Science", "Python"]
    ]

    tech_in_motion_executer(base_url, parameters, testmode=testmode)


if __name__ == "__main__":
    tech_in_motion_reader(testmode=False)
