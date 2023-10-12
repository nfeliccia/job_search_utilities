"""
The purpose of this script is to open pages of interest on the Tech in Motion website. This script will open the Tech"""

from selenium import webdriver


def open_tech_in_motion_urls(driver: webdriver.Chrome):
    """
    Opens the Tech in Motion URLs for job search. Note motion recruitment uses url based search parameters.

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
    urls.append("https://motionrecruitment.com/tech-jobs?specialties=machine-learning-data-science&remote=true")
    urls.append("https://techinmotion.com/upcoming-events")

    for url in urls:
        driver.execute_script(f"window.open('{url}','_blank');")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    open_tech_in_motion_urls(driver)
    input("Press Enter to continue...")
    driver.quit()

# Path: Source/tech_in_motion_reader.py
