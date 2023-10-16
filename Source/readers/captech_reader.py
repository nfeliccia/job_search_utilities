from typing import Iterable

from readers import initialize_webdriver
from readers.readers_common import construct_url, close_with_test


def captech_executer(parameters: Iterable[dict] = None, testmode=False):
    # Initialize the web driver
    driver = initialize_webdriver()

    # set base url
    base_url = "https://www.captechconsulting.com/careers/current-openings/"

    # Open the job openings page for Philadelphia (location=253788)

    urls = [construct_url(base_url=base_url, query_params=x) for x in parameters]
    for url in urls:
        # Open a new tab
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        driver.execute_script(window_open_script)

    close_with_test(driver=driver, testmode=testmode)


def captech_reader(testmode=False):
    parameters = [{"keywords": "", "location": "253788", "page": "1", },
                  {"keywords": "Machine Learning", "page": "1", },
                  {"keywords": "Data Science", "page": "1", },
                  {"keywords": "Python", "page": "1", }]
    captech_executer(parameters, testmode=testmode)


# Uncomment the below line when you want to execute the script

if __name__ == "__main__":
    captech_reader(testmode=False)
