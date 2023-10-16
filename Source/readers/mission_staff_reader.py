from selenium.webdriver.common.by import By

from readers import initialize_webdriver


def mission_staff_reader(testmode=False) -> None:
    """
    Reads the Mission Staff job listings.

    Args:
        testmode: Run in test mode or user mode. Test mode will auto close the browser window.
    """
    # Set up the Selenium driver (you might need to adjust the path and options based on your setup)
    driver = initialize_webdriver()

    # Open the website
    driver.get('https://missionstaff.com/careers/#/')

    # Wait for 3 seconds
    driver.implicitly_wait(3)

    # Find the "Technology" button using the data-automation-id attribute and click it
    technology_ = '[data-automation-id="Technology (9)"]'
    technology_button = driver.find_element(By.CSS_SELECTOR, value=technology_)
    technology_button.click()

    if not testmode:
        # Prompt the user to press Enter to keep the window open
        input("Press any key to continue...")
    # Close the driver when done
    driver.quit()


if __name__ == "__main__":
    print(f"Starting...{__file__}")
    mission_staff_reader(testmode=False)
    print(f"Finished {__file__} !")
