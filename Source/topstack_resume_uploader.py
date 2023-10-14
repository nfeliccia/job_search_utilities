from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Data.reference_values import actual_values

"""
Note. This is incomplete. When the resume is on file we have to select "Upload Resume" 

"""


def open_primary_page(driver: webdriver.Chrome):
    """

    Args:
        driver: Chrome Webdriver

    Returns:
        None

    """
    print("Opening the provided URL...")
    driver.get("https://jobs.topstackgroup.com/index.smpl?arg=user_login")


def main():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    SLEEPTIME = 1

    try:
        # Open the provided URL
        open_primary_page(driver)
        sleep(SLEEPTIME * 3)
        # Click the "Use Password" link
        print("Clicking the 'Use Password' link...")
        use_password_link = driver.find_element(By.XPATH, "//a[contains(text(),'Use Password')]")
        use_password_link.click()
        print("Waiting for the password input to become visible...")
        sleep(SLEEPTIME * 3)
        # Wait for the password input to become visible
        password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
        )
        print("Entering the password...")
        password_input.send_keys("g6r^53#sDvf3HLXk")
        sleep(SLEEPTIME * 3)

        # Enter the email address
        print("Entering the email address...")
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("nic@secretsmokestack.com")
        sleep(SLEEPTIME)
        # Click the "Submit" butto
        print("Clicking the 'Submit' button...")
        submit_button = driver.find_element(By.XPATH, "//a[@name='login']")
        submit_button.click()

        # Wait for the next page to load by waiting for the unique meta content
        # WebDriverWait(driver, 20).until(
        #    EC.presence_of_element_located((By.XPATH, "//meta[@content='Looking for a job in Wayne, PA? We can help!']"))
        # )
        sleep(SLEEPTIME * 3)

        # Click the "My Account" link
        my_account_link = driver.find_element(By.XPATH, "//a[contains(@href, 'jb_user_account')]")
        my_account_link.click()

        # Click the "Resume" link
        resume_link = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '#jb-user-resume')]"))
        )
        resume_link.click()

        sleep(SLEEPTIME * 3)
        resume_path = str(actual_values.current_resume_path)

        # Find the file input element and send the path to the resume
        file_input = driver.find_element(By.ID, "upload")
        file_input.send_keys(resume_path)

        sleep(SLEEPTIME * 3)
        # Click the resume submit button
        resume_button = driver.find_element(By.XPATH, '//*[@id="resumeBtn"]')
        resume_button.click()
        # Pause for demonstration purposes (You can remove this line in actual usage)
        input("Press Enter to close the browser...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
