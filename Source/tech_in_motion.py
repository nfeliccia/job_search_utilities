import argparse
import os

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

import reference_values
from tech_in_motion_reader import open_tech_in_motion_urls

ACTUAL_VALUES = reference_values.actual_values
DUMMY_VALUES = reference_values.dummy_values
"""
The purpose of this script is to automate the job application process for Motion Recruitment. This script will open
the Tech in Motion job search page and the Tech in Motion events page. It will also fill out the candidate resume
submission form and submit it. The form is not submitted by default. You must pass the --submit flag to submit the
form. The form will not be submitted if the captcha is not solved. The captcha must be solved manually. The form
will not be submitted if the captcha is not solved. The captcha must be solved manually. 
"""



def fill_form_and_submit(driver: selenium.webdriver, user_data: reference_values.ReferenceValues, submit: bool = False):
    """
    The purpose of this function is to fill out the form and submit it. BY It we mean the candidate resume submitssion
    form on the Motion Recruitment website. This function will not work if the form has changed. The dropdowns do not
    work but that doesnt stop you from submitting the form..

    Args:
        driver: selenium.webdriver
        user_data: User data in the form of a ReferenceValues dataclass
        submit: Boolean whether or not to submit. Here for testing purposes.

    Returns:

    """
    driver.get('https://motionrecruitment.com/candidates')
    # Click on submit a resume button
    submit_resume_button = driver.find_element(By.XPATH, value='//button[text()="Submit a resume"]')
    submit_resume_button.click()
    try:
        # Fill out the form
        driver.find_element(By.XPATH, '//*[@id="first-name"]').send_keys(user_data.first_name)
        driver.find_element(By.XPATH, '//*[@id="last-name"]').send_keys(user_data.last_name)
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(user_data.email)
        driver.find_element(By.XPATH, '//*[@id="phone"]').send_keys(user_data.phone)
        crp = os.path.abspath(user_data.current_resume_path)
        driver.find_element(By.XPATH, '//*[@id="resumeInput"]').send_keys(str(crp))

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
    user_data = ACTUAL_VALUES if use_real_data else DUMMY_VALUES
    driver = webdriver.Chrome()
    open_tech_in_motion_urls(driver)
    fill_form_and_submit(driver, user_data, submit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automation for Motion Recruitment job applications.')
    parser.add_argument('--use_real_data', action='store_true', help='Use real user data for submission')
    parser.add_argument('--submit', action='store_true', help='Actually submit the application form')

    parser.add_argument('--open-urls', action='store_true',
                        help='Open Tech in Motion URLs for job search without any other action.')
    args = parser.parse_args()
    if args.open_urls:
        driver = webdriver.Chrome()
        open_tech_in_motion_urls(driver)
        input("Press enter when done. ")
        driver.quit()
        exit()

    main(args.use_real_data, args.submit)
