import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_tandymtech_url():
    # Configure the Selenium webdriver (assuming Chrome in this example, but this can be adjusted)
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Navigate to the specified URL
    driver.get(
            "https://tandymtech.com/job-seekers/tech-search-results/?keyword=&where=19124,%20Philadelphia,%20Pennsylvania")

    try:
        # Wait for up to 10 seconds for the button to appear
        eu_conf_button = '//*[@id="hs-eu-confirmation-button"]'
        located = EC.presence_of_element_located((By.XPATH, ('%s' % eu_conf_button)))
        button = WebDriverWait(driver, 10).until(located)
        # If button found, click on it
        time.sleep(5)
        print("Before clicking")
        button.click()
        print("After clicking")
        input("Press Enter to continue...")

    except Exception as e:
        # If button is not found within 10 seconds, print an error message
        print(f"Something went wrong {e}")
        raise Exception

    # Note: You might want to add more actions or close the browser after a certain action
    # For now, I'll keep the browser open
    # driver.close()


if __name__ == "__main__":
    open_tandymtech_url()
