from selenium import webdriver


def create_captech_url(keyword=None, location=None):
    base_url = "https://www.captechconsulting.com/careers/current-openings?"

    if keyword:
        keyword = "%20".join(keyword.split())
        base_url += f"keywords={keyword}&"

    if location:
        base_url += f"location={location}&"

    return base_url + "page=1"


def captech_reader(testmode=False):
    # Initialize the web driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the main job openings page
    driver.get(create_captech_url())

    # Open the job openings page for Philadelphia (location=253788)
    blank_ = "window.open('', '_blank');"
    handles_ = driver.window_handles[-1]
    driver.execute_script(blank_)
    driver.switch_to.window(handles_)
    driver.get(create_captech_url(location="253788"))

    # Open tabs for specified keywords
    keywords = ["Machine Learning", "Data Science", "Python"]
    for keyword in keywords:
        driver.execute_script(blank_)
        driver.switch_to.window(handles_)
        url = create_captech_url(keyword=keyword)
        driver.get(url)

    if not testmode:
        input("Press Enter to close the browser...")

    driver.quit()


# Uncomment the below line when you want to execute the script

if __name__ == "__main__":
    captech_reader(testmode=False)
