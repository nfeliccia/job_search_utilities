"""This script automates the process of searching for jobs at Susquehanna International Group.

It uses Selenium WebDriver to navigate to the careers page of Susquehanna International Group,
searches for jobs based on specified keywords, and optionally interacts with elements on the page,
such as checkboxes for filtering job locations.

Keywords for job searches are defined within the script, and the WebDriver will open a new browser
tab for each keyword, perform the search, and interact with the page as defined in the script."""
import urllib.parse

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def susquehanna_international_reader():
    """
    Navigates to the careers page of Susquehanna International Group and performs job searches based on predefined keywords.

    The function uses Selenium WebDriver to open a new browser window, perform job searches for each keyword,
    and interacts with elements on the page (e.g., checking checkboxes for job location filters).
    It performs these actions iteratively for each keyword defined within the function.
    """

    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Define the base URL and keywords
    base_url = "https://careers.sig.com/search-results?keywords={}"
    keywords = ['"Data Science"', '"Machine Learning"', '"Python"']

    for keyword in keywords:
        driver.execute_script("window.open('', '_blank');")  # Open a new blank tab
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab
        url_format = base_url.format(urllib.parse.quote(keyword))
        print(url_format)
        driver.get(url_format)

        # Wait for the page to load and check for the "Allow" button in the cookie popup, then click it
        try:
            element_xpath = '/html/body/div[1]/section[1]/div/div/div/div[2]/button'
            element_located = EC.presence_of_element_located((By.XPATH, element_xpath))
            allow_button = WebDriverWait(driver, 2).until(element_located)
            allow_button.click()

        except (NoSuchElementException, TimeoutException) as _:
            print(f"Cookie consent popup not found or handled for tab with keyword: {keyword}")

        try:
            # Add an explicit wait for the checkbox element to be visible
            child__checkbox = "#JobLocationBody li:nth-child(1) .checkbox"
            checkbox_element_locator = (By.CSS_SELECTOR, child__checkbox)
            located = EC.visibility_of_element_located(checkbox_element_locator)
            checkbox = WebDriverWait(driver, timeout=10).until(located)
            checkbox.click()
        except NoSuchElementException as _:
            print(f"Checkbox not found in tab with keyword: {keyword} ")

    # Prompt the user to press Enter to keep the window open
    input("Press Enter to close the browser...")

    # Close the browser
    driver.quit()


if __name__ == '__main__':
    susquehanna_international_reader()
