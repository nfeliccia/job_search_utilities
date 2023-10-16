from typing import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readers import initialize_webdriver, construct_url
from readers.readers_common import close_with_test


def collabera_executer(parameters: Iterable[dict] = None, testmode=False):
    driver = initialize_webdriver()
    base_url = "https://collabera.com/job-search/"

    urls = [construct_url(base_url=base_url, query_params=x) for x in parameters]
    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        driver.execute_script(window_open_script)
        located = EC.presence_of_element_located((By.CSS_SELECTOR, 'header.header a.navbar-brand'))
        WebDriverWait(driver, 10).until(located)

    close_with_test(driver=driver, testmode=testmode)


def collabera_reader(testmode=False):
    parameters = [
        {"sort_by": 'dateposted', "industry": '', "keyword": 'Python', "Posteddays": '0'},
        {"sort_by": 'dateposted', "industry": '', "keyword": 'Data+Science', "Posteddays": '0'},
        {"sort_by": 'dateposted', "industry": '', "keyword": 'Machine+Learning', "Posteddays": '0'}]

    collabera_executer(parameters, testmode=testmode)


if __name__ == '__main__':
    collabera_reader(testmode=False)
