import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Data.reference_values import actual_values, dummy_values


def main(use_actual_data):
    # Determine which set of values to use based on the command line argument
    values_to_use = actual_values if use_actual_data else dummy_values

    # Setup Selenium web driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the provided URL
    driver.get("https://tandym-portal.bullhorncloud.com/#/signup/000/init")

    # Wait for a second and print a message
    driver.implicitly_wait(1)
    print("Website successfully opened")

    # Upload the resume
    upload_element = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_element.send_keys(str(values_to_use.current_resume_path))

    # Handle the next button click
    try:
        # Wait up to 10 seconds for the next button to be clickable
        next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.nextSectionIcon.glyphicon.glyphicon-arrow-right")))
        next_button.click()
    except Exception as e:
        # If the regular click fails, try a JavaScript click
        print(e)
        driver.execute_script("arguments[0].click();", next_button)

    # Wait for the page title to contain the specified text
    WebDriverWait(driver, 30).until(EC.title_contains("The Tandym Group Candidate Portal"))

    # Wait for the form container to be visible (Solution 3)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".form-container")))

    # Fill in the forms for First Name using alternative locators (Solution 2)
    first_name = driver.find_element(By.CSS_SELECTOR, "input[name='firstName']")
    first_name.click()
    first_name.send_keys(values_to_use.first_name)

    # Wait for the lastName element to be visible and then send keys
    last_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "lastName")))
    last_name.send_keys(values_to_use.last_name)

    # Send keys directly to email and mobilePhone elements
    driver.find_element(By.NAME, "email").send_keys(values_to_use.email)
    driver.find_element(By.NAME, "mobilePhone").send_keys(values_to_use.phone)

    # Click the select2 container to open the dropdown for Current Employment Status
    dropdown_container = driver.find_element(By.CSS_SELECTOR, ".select2-container")
    dropdown_container.click()

    # Wait for the dropdown list to be displayed
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".select2-drop")))

    # Click the desired option
    option = driver.find_element(By.XPATH, "//li[text()='Employed as a consultant or temporary staff']")
    option.click()

    # Add a press enter prompt before quitting the driver
    input("Press Enter to continue...")
    driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tandym Resume Uploader Script")
    parser.add_argument('--use_actual_data', action='store_true', default=False,
                        help='Use actual data if true, otherwise use dummy data.')
    args = parser.parse_args()
    main(args.use_actual_data)
