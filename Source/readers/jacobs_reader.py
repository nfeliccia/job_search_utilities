import urllib.parse

from . import webdriver


def create_jacobs_url(keyword: str) -> str:
    """Constructs a URL for job search on the Jacobs Communications website with the given keyword."""

    base_url = "https://careers.jacobs.com/job-search-results/"

    # Parameters for the URL
    params = {
        'keyword': keyword,
        'location': 'Philadelphia, PA, USA',
        'latitude': '39.9525839',
        'longitude': '-75.1652215',
        'radius': '50'
    }

    # Encoding the parameters and appending to the base URL
    url = base_url + "?" + urllib.parse.urlencode(params)

    return url


def jacobs_reader(testmode=False):
    keywords = ["Data Scientist Associate", "Data Scientist Lead", "Data Scientist", "Machine Learning", "Python"]

    # Initialize the webdriver (assuming Chrome, but can be changed)
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open a blank tab
    driver.get("about:blank")

    for keyword in keywords:
        url = create_jacobs_url(keyword)
        print(url)
        window_open_script = f"window.open('{url}');"  # Open a new tab with the URL
        driver.execute_script(window_open_script)
        driver.implicitly_wait(1.5)

    if not testmode:
        input("Press Enter to quit...")
    driver.close()
    driver.quit()


if __name__ == "__main__":
    jacobs_reader()
