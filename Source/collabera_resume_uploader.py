"""
Automates the application submission process on the Collabera website.
The script:
- Opens the Collabera resume submission page.
- Optionally clicks an accept button if present.
- Fills out the application form with either real or dummy personal details.
- Uploads a resume.
- Optionally submits the form after the user completes a CAPTCHA.
"""
import argparse
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import reference_values

ACTUAL_VALUES = reference_values.actual_values
DUMMY_VALUES = reference_values.dummy_values


def collabera_apply(driver: webdriver.Chrome = None, values: reference_values.ReferenceValues = None,
                    submit: bool = False):
    """
    Automates the Collabera application process.
    
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        values (ReferenceValues): Dataclass containing applicant details.
        submit (bool): Whether to actually submit the form after filling it.
    
    Behavior:
    - Opens the Collabera resume submission page and maximizes it.
    - Clicks a site acceptance button if present.
    - Fills out the application form with the provided values.
    - Uploads the resume from the provided path.
    - If `submit` is True, waits for the user to complete a CAPTCHA and submits the application.
    """

    # Open Collabera resume submission page
    driver.get("https://collabera.com/submit-resume/")
    driver.maximize_window()
    time.sleep(3)  # wait for the page to load

    # Click the button if it exists
    try:
        accept_all_button = driver.find_element(By.XPATH, '//*[@id="wt-cli-accept-all-btn"]')
        accept_all_button.click()
    except NoSuchElementException:
        pass

    # Fill in the required fields
    print("Filling in the form...")
    print("First name: " + values.first_name)
    print("Resume path: " + str(values.current_resume_path))
    driver.find_element(By.XPATH, '//*[@id="firstname"]').send_keys(values.first_name)
    time.sleep(0.1)
    driver.find_element(By.XPATH, '//*[@id="lastname"]').send_keys(values.last_name)
    print("Last name: " + values.last_name)
    time.sleep(0.1)
    driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(values.email)
    print("Email: " + values.email)
    time.sleep(0.1)
    driver.find_element(By.XPATH, '//*[@id="number"]').send_keys(values.phone)
    print("Phone: " + values.phone)
    time.sleep(0.1)
    driver.find_element(By.XPATH, '//*[@id="linprofile"]').send_keys(values.linkedin_url)
    print("LinkedIn URL: " + values.linkedin_url)
    time.sleep(0.1)

    # Click the checkbox if unchecked
    checkbox = driver.find_element(By.XPATH, '//*[@id="exampleCheck3"]')
    time.sleep(0.1)
    if not checkbox.is_selected():
        checkbox.click()

    # Click on the upload button and provide the resume path
    file_input = driver.find_element(By.CLASS_NAME, "wpcf7-drag-n-drop-file")
    resume_file_path = str(values.current_resume_path)
    file_input.send_keys(resume_file_path)

    if submit:
        # Wait for the user to complete the captcha
        input("Please complete the CAPTCHA and then press Enter to continue...")

        submit_button = driver.find_element(By.XPATH, '//*[@id="wpcf7-f8654-o1"]/div[7]/p/button')
        submit_button.click()


def main():
    """
    Main driver function of the script.
    Parses command-line arguments, initializes the WebDriver, and starts the application process.
    At the end, waits for the user to press enter before closing the browser and quitting the driver.
    """

    parser = argparse.ArgumentParser(description="Automate Collabera job application.")
    parser.add_argument('--use_real_data', action='store_true', help='Use real user data for submission')
    parser.add_argument('--submit', action='store_true', help='Actually submit the application form')

    args = parser.parse_args()

    # Setup WebDriver
    driver = webdriver.Chrome()

    # Apply
    values_to_use = ACTUAL_VALUES if args.use_real_data else DUMMY_VALUES
    submit_resume = args.submit
    collabera_apply(driver=driver, values=values_to_use, submit=submit_resume)

    input("Press enter when done. ")
    driver.quit()


if __name__ == "__main__":
    main()
