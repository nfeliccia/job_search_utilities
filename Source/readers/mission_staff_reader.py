from selenium.webdriver.common.by import By

from readers import GeneralReader


def mission_staff_reader(testmode=False) -> None:
    """
    Reads the Mission Staff job listings.

    Args:
        testmode: Run in test mode or user mode. Test mode will auto close the browser window.
    """

    # Create a GeneralReader object.
    reader = GeneralReader()

    # Open the Mission Staff website.
    reader.webdriver.get('https://missionstaff.com/careers/#/')

    # Wait for 3 seconds.
    reader.webdriver.implicitly_wait(3)

    # Find the "Technology" button using the data-automation-id attribute and click it.
    technology_ = '[data-automation-id="Technology (9)"]'
    technology_button = reader.webdriver.find_element(By.CSS_SELECTOR, value=technology_)
    technology_button.click()

    # Close the web browser.
    reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    mission_staff_reader(testmode=False)
