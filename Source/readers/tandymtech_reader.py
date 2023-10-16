"""
This script automates the process of navigating to two specific URLs using Selenium.
For each URL, the script performs the following actions:
1. Opens the URL in a Chrome browser.
2. Waits for and clicks on the 'hs-eu-confirmation-button'.
3. For the second URL, checks a specific checkbox if it's not already checked.
4. Waits for the user to press Enter and then quits the browser.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from readers import initialize_webdriver


def click_confirmation_button(driver: webdriver.Chrome, eu_conf_button_xpath: str) -> None:
    """
    Waits for and clicks on the 'hs-eu-confirmation-button' using the provided webdriver.
    
    Args:
        driver (webdriver.Chrome): The Chrome webdriver instance.
        eu_conf_button_xpath (str): The XPATH for the 'hs-eu-confirmation-button'.
    """
    try:
        located = EC.presence_of_element_located((By.XPATH, eu_conf_button_xpath))
        button = WebDriverWait(driver, 10).until(located)
        time.sleep(2)  # Give the button a moment to be clickable
        button.click()
    except Exception as e:
        print(f"Error clicking hs-eu-confirmation-button: {e}")


def open_url_in_new_tab(driver: webdriver.Chrome, url: str) -> None:
    """
    Opens a new browser tab and navigates to the specified URL.
    
    Args:
        driver (webdriver.Chrome): The Chrome webdriver instance.
        url (str): URL to navigate to.
    """
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the last opened tab
    driver.get(url)


def tandym_tech_reader(testmode=True) -> None:
    """

    This script automates the process of navigating to two specific URLs using Selenium.
    For each URL, the script performs the following actions:
    1. Opens the URL in a Chrome browser.
    2. Waits for and clicks on the 'hs-eu-confirmation-button'.
    3. For the second URL, checks a specific checkbox if it's not already checked.
    4. Waits for the user to press Enter and then quits the browser.


    Args:
        testmode: RUn in test mode.

    Returns:

    """
    driver = initialize_webdriver()

    # Navigate to the first URL and click the confirmation button
    pennsylvania = ("https://tandymtech.com/job-seekers/tech-search-results/?keyword=&where=19124,%20Philadelphia,"
                    "%20Pennsylvania")
    driver.get(pennsylvania)
    time.sleep(3)
    eu_button = '//*[@id="hs-eu-confirmation-button"]'
    click_confirmation_button(driver, eu_button)

    # Navigate to the second URL in a new tab and click the confirmation button
    open_url_in_new_tab(driver, "https://tandymtech.com/job-seekers/tech-search-results/?keyword=(Remote)&where=")
    click_confirmation_button(driver, eu_button)

    scroll_to_bottom_of_section(driver, ".cards")
    click_load_more_until_end(driver, "Load more")

    if not testmode:
        input("Press Enter to quit...")

    else:
        driver.quit()


def scroll_to_bottom_of_section(driver: webdriver.Chrome, css_selector: str) -> None:
    """
    Scrolls to the bottom of a specified section using its CSS selector.

    Args:
        driver (webdriver.Chrome): The Chrome webdriver instance.
        css_selector (str): CSS selector of the section to scroll.
    """
    try:
        element = driver.find_element_by_css_selector(css_selector)
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", element)
    except Exception as e:
        print(f"Error scrolling to the bottom of the section: {e}")


def click_load_more_until_end(driver: webdriver.Chrome, load_more_text: str) -> None:
    """
    Continuously clicks on an element with the specified text until it's no longer present or clickable.

    Args:
        driver (webdriver.Chrome): The Chrome webdriver instance.
        load_more_text (str): Text of the element to click.
    """
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{load_more_text}')]"))
            )
            load_more_button.click()
            time.sleep(2)  # Wait for the page to load new content
        except Exception:
            # If the button is not found or not clickable, break the loop
            break


if __name__ == "__main__":
    tandym_tech_reader()
