import time

import reference_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

SLEEP_TIME = 0.5


def open_tech_in_motion_urls():
    # Base URL
    BASE_URL = "https://motionrecruitment.com/tech-jobs?radius=25&search-city=19124&postalcode=19124&remote=true&location-display-name=Philadelphia%2C+Pennsylvania+19124%2C+United+States&start=0"

    # Keywords for different job types
    KEYWORDS = ["Machine+Learning", "Data+Science", "Python"]

    # URLs to open
    urls = [f"{BASE_URL}&keywords={keyword}" for keyword in KEYWORDS]
    urls.append("https://techinmotion.com/upcoming-events")

    # Start Chrome browser
    driver = webdriver.Chrome()

    # Open each URL in a new tab
    for url in urls:
        driver.execute_script(f"window.open('{url}', '_blank');")
    # Keep the script running until you press Enter

    input("Press Enter to close the browser and exit the script...")
    driver.quit()


def submit_resume():
    driver = webdriver.Chrome()

    # Opening the URL
    print("Opening the URL...")
    driver.get('https://motionrecruitment.com/candidates')
    time.sleep(SLEEP_TIME)

    # Clicking the button
    print("starting dropdown")
    driver.find_element(By.XPATH, '//*[@id="hs_cos_wrapper_widget_1672155533981"]/button').click()
    time.sleep(SLEEP_TIME)

    # Setting location dropdown to "Philadelphia"
    wait = WebDriverWait(driver, timeout=10)
    custom_location_select = wait.until(EC.element_to_be_clickable((By.ID, "custom-location-select")))
    location_dropdown = Select(custom_location_select)
    location_dropdown.select_by_value('19107')

    # Setting Tech Sector dropdown to "Data"
    print("Setting Tech Sector dropdown to  Data")
    wait = WebDriverWait(driver, timeout=10)
    custom_category_select = wait.until(EC.element_to_be_clickable((By.ID, "custom-category-select")))
    sector_dropdown = Select(custom_category_select)
    sector_dropdown.select_by_value('Data')
    time.sleep(SLEEP_TIME)

    # Filling out the form fields
    driver.find_element(By.XPATH, value='//*[@id="first-name"]').send_keys(reference_values.first_name)
    time.sleep(SLEEP_TIME)
    driver.find_element(By.XPATH, value='//*[@id="last-name"]').send_keys(reference_values.last_name)
    time.sleep(SLEEP_TIME)
    driver.find_element(By.XPATH, value='//*[@id="email"]').send_keys(reference_values.email)
    time.sleep(SLEEP_TIME)
    driver.find_element(By.XPATH, value='//*[@id="phone"]').send_keys(reference_values.phone)
    time.sleep(SLEEP_TIME)

    # Uploading the resume
    rvcrp_str = str(reference_values.current_resume_path)
    driver.find_element(By.XPATH, '//*[@id="resumeInput"]').send_keys(rvcrp_str)
    time.sleep(SLEEP_TIME)

    print("Click the Captcha Box and solve the Captcha. Then press Enter to continue...")
    input()

    # Clicking the submit button
    submit_button_path = '//*[@id="hs_cos_wrapper_widget_1672155533981"]/div/div/div[1]/form/div/div[5]/input'
    submit_button = driver.find_element(By.XPATH, submit_button_path)
    if not submit_button.get_attribute("disabled"):
        submit_button.click()
    else:
        print("Submit button is disabled. Form might not be filled out correctly or captcha was not solved.")


submit_resume()
