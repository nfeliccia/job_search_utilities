import time

from selenium import webdriver


def create_url(keyword):
    base_url = ("https://collabera.com/job-search/?sort_by=dateposted&industry=&keyword={"
                "keyword}&location=19124&Posteddays=0")
    split = keyword.split()
    formatted_keyword = '+'.join(split)
    url_format = base_url.format(keyword=formatted_keyword)
    return url_format


def collabera_reader():
    keywords = ["Python", "Machine Learning", "Data Science"]
    urls = [create_url(keyword) for keyword in keywords]

    driver = webdriver.Chrome()

    for i, url in enumerate(urls):
        if i == 0:
            driver.get(url)
        else:
            driver.execute_script(f"window.open('{url}','_blank');")
        time.sleep(2)  # give the browser time to open the tab

    input("Hit Enter to close the browser...")
    driver.quit()


if __name__ == '__main__':
    collabera_reader()
