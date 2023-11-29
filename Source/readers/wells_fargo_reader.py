from time import sleep

from playwright.sync_api import Page

from Data.reference_values import universal_search_terms
from common_code import GeneralReaderPlaywright


class WellsFargoReader(GeneralReaderPlaywright):
    wells_fargo_primary_jobs = "https://www.wellsfargojobs.com/"

    def __init__(self, testmode: bool = False, qth: str = None):
        super().__init__(root_website=self.wells_fargo_primary_jobs, testmode=testmode)
        self.qth = qth

    def initial_tab(self):
        it_page = self.create_new_tab()
        self.safe_click(it_page.get_by_role("button", name="Accept All"), timeout=3000)
        it_page.get_by_role("link", name="Jobs", exact=True).click()
        return it_page

    def search_keyword(self, in_page: Page = None, keyword: str = None):
        """
        This searches for a keyword and returns the page content.
        Args:
            keyword:

        Returns:
            str: page content html in string form.

        """

        in_page.click('a[data-toggle="collapse"][href="#country-Collapse"]')
        in_page.wait_for_selector('textarea.select2-search__field')

        # Then, click on the element
        in_page.click('textarea.select2-search__field')
        in_page.get_by_role("option", name="United States of America").click()
        in_page.get_by_placeholder("Search jobs").click()
        in_page.get_by_placeholder("Search jobs").fill(keyword)
        in_page.wait_for_selector('button#js-main-job-search')
        in_page.click('button#js-main-job-search')
        sleep(3)


def wells_fargo_reader(testmode: bool = False):
    with WellsFargoReader(testmode=testmode) as wf_reader:
        for keyword in universal_search_terms:
            jobs_page = wf_reader.initial_tab()
            wf_reader.search_keyword(in_page=jobs_page, keyword=keyword)
        wf_reader.close_with_test(testmode=testmode)


if __name__ == "__main__":
    wells_fargo_reader(testmode=False)

"""
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.wellsfargojobs.com/")
    
    page.get_by_role("link", name="Jobs", exact=True).click()
    
    page.get_by_role("button", name="Worker Type").click()
    page.get_by_placeholder("Choose Worker Type").click()
    page.get_by_placeholder("Choose Worker Type").press("Escape")

    page.get_by_placeholder("Search jobs").press("Enter")
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").fill("\"Machine Learning\"")
    page.get_by_placeholder("Search jobs").press("Enter")
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").click()
    page.get_by_placeholder("Search jobs").press("Shift+Enter")
    page1 = context.new_page()
    page1.goto("https://www.wellsfargojobs.com/en/jobs/?search=%22Machine+Learning%22&country=United+States+of+America&pagesize=20#results")
    page1.get_by_placeholder("Search jobs").click()
    page1.get_by_placeholder("Search jobs").click()
    page1.get_by_placeholder("Search jobs").fill("Python")
    page1.get_by_placeholder("Search jobs").press("Enter")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

"""
