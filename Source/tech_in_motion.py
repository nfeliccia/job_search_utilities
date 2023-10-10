import argparse
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

import reference_values

CURRENT_VALUES = reference_values.actual_values
DUMMY_VALUES = reference_values.dummy_values


def open_tech_in_motion_urls(driver: webdriver.Chrome):
    """
    Opens the Tech in Motion URLs for job search.

    Args:
        driver (webdriver.Chrome): The Chrome driver instance.

    Returns:
        None
    """
    # Base URL
    BASE_URL = ("https://motionrecruitment.com/tech-jobs?radius=25&search-city=19124&postalcode=19124&remote=true"
                "&location-display-name=Philadelphia%2C+Pennsylvania+19124%2C+United+States&start=0")

    # Keywords for different job types
    KEYWORDS = ["Machine+Learning", "Data+Science", "Python"]

    # URLs to open
    urls = [f"{BASE_URL}&keywords={keyword}" for keyword in KEYWORDS]
    urls.append("https://techinmotion.com/upcoming-events")

    for url in urls:
        driver.execute_script(f"window.open('{url}','_blank');")


def fill_form_and_submit(driver, user_data, submit: bool = False):
    driver.get('https://motionrecruitment.com/candidates')
    # Click on submit a resume button
    submit_resume_button = driver.find_element(By.XPATH, value='//button[text()="Submit a resume"]')
    submit_resume_button.click()
    try:
        # Fill out the form
        first_name_input = driver.find_element(By.XPATH, '//*[@id="first-name"]')
        last_name_input = driver.find_element(By.XPATH, '//*[@id="last-name"]')
        email_input = driver.find_element(By.XPATH, '//*[@id="email"]')
        phone_input = driver.find_element(By.XPATH, '//*[@id="phone"]')
        resume_input = driver.find_element(By.XPATH, '//*[@id="resumeInput"]')

        first_name_input.send_keys(user_data.first_name)
        last_name_input.send_keys(user_data.last_name)
        email_input.send_keys(user_data.email)
        phone_input.send_keys(user_data.phone)
        resume_input.send_keys(str(os.path.abspath(user_data.current_resume_path)))

        print("Click the Captcha Box and solve the Captcha. Then press Enter to continue...")
        input()

        if submit:
            # Click the submit button
            submit_button_path = '//*[@id="hs_cos_wrapper_widget_1672155533981"]/div/div/div[1]/form/div/div[5]/input'
            submit_button = driver.find_element(By.XPATH, submit_button_path)
            if not submit_button.get_attribute("disabled"):
                submit_button.click()
            else:
                print("Submit button is disabled. Form might not be filled out correctly or captcha was not solved.")
    except Exception as e:
        print(f"Failed to fill out the form or submit. Error: {e}")


def main(use_real_data: bool, submit: bool):
    user_data = CURRENT_VALUES if use_real_data else DUMMY_VALUES
    driver = webdriver.Chrome()
    # open_tech_in_motion_urls(driver)
    fill_form_and_submit(driver, user_data, submit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automation for Motion Recruitment job applications.')
    parser.add_argument('--use_real_data', action='store_true', help='Use real user data for submission')
    parser.add_argument('--submit', action='store_true', help='Actually submit the application form')
    args = parser.parse_args()

    main(args.use_real_data, args.submit)
