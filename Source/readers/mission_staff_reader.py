from selenium import webdriver
from selenium.webdriver.common.by import By


def mission_staff_reader() -> None:
    """
    Reads the Mission Staff job listings.
    """
    # Set up the Selenium driver (you might need to adjust the path and options based on your setup)
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the website
    driver.get('https://missionstaff.com/careers/#/')

    # Wait for 3 seconds
    driver.implicitly_wait(3)

    # Find the "Technology" button using the data-automation-id attribute and click it
    technology_button = driver.find_element(By.CSS_SELECTOR, '[data-automation-id="Technology (9)"]')
    technology_button.click()

    print("Press any key to continue...")
    # Close the driver when done
    driver.quit()


if __name__ == "main":
    mission_staff_reader()
