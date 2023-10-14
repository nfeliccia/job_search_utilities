from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_collabera_url(keyword):
    website_job_search = "https://collabera.com/job-search/"
    argument = "?sort_by=dateposted&industry=&keyword={keyword}&location=19124&Posteddays=0"
    base_url = website_job_search + argument
    formatted_keyword = '+'.join(keyword.split())
    url_format = base_url.format(keyword=formatted_keyword)
    return url_format


def collabera_reader(testmode=False):
    driver = webdriver.Chrome()
    driver.maximize_window()

    keywords = ["Python", "Machine Learning", "Data Science"]
    for keyword in keywords:
        driver.execute_script("window.open('', '_blank');")  # Open a new blank tab
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the newly opened tab
        url_format = create_collabera_url(keyword)
        print(url_format)
        driver.get(url_format)
        located = EC.presence_of_element_located((By.CSS_SELECTOR, 'header.header a.navbar-brand'))
        WebDriverWait(driver, 10).until(located)

    if not testmode:
        input("Hit Enter to close the browser...")
    driver.quit()


if __name__ == '__main__':
    collabera_reader(testmode=False)
