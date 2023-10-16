import typing

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readers import initialize_webdriver, construct_url
from readers.readers_common import close_with_test


def topgolf_executer(parameters: typing.Iterable[dict], testmode=False):
    """

    Args:
        parameters: parameters for the strings
        testmode: boolean to determine if the browser should be closed after the test is complete

    Returns:
        None

    """
    # Initialize the web driver. Make sure the chromedriver executable is in your PATH.
    driver = initialize_webdriver()
    base_url = "https://careers.topgolf.com/jobs/"
    urls = [construct_url(base_url=base_url, query_params=x) for x in parameters]

    for url in urls:
        print(url)
        window_open_script = f"window.open('{url}', '_blank');"
        driver.execute_script(window_open_script)

        try:
            # Wait for the cookie consent button to be clickable, and click it
            wait = WebDriverWait(driver, 3)
            cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "cookie-consent-accept-button")))
            cookie_button.click()
        except Exception as e:
            print(f"An error occurred while waiting for the cookie consent button: {e}")

    close_with_test(testmode=testmode, driver=driver)


def topgolf_reader():
    parameters = [{"page": "1", "categories": "Technology Innovation / IT"},
                  {"lat": "40.0228352", "lng": "-75.0911", "radius": "15", "page": "1", "radiusUnit": "MILES"}]

    topgolf_executer(parameters, testmode=False)


if __name__ == "__main__":
    topgolf_reader()
