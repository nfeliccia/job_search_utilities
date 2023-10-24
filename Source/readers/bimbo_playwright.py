import re

from playwright.sync_api import sync_playwright, Page, expect

BIMBO_URL = "https://careers.bimbobakeriesusa.com/en-US/search"


def has_title(page: Page):
    q = expect(page).to_have_title(re.compile("Opportunities at Bimbo Bakeries USA"))
    return q


playwright_ = sync_playwright().start()
browser = playwright_.chromium.launch(headless=False)
page_ = browser.new_page()
page_.goto(BIMBO_URL)
result = has_title(page_)
page_.get_by_label("Keyword").fill("Python")
page_.get_by_label("Keyword").press("Enter")

page_b = browser.new_page()
page_b.goto(BIMBO_URL)
page_b.get_by_label("Keyword").fill(''"Data Science"'')
page_b.get_by_label("Location").fill("Philadelphia, PA 19124, USA")
page_b.get_by_label("Keyword").press("Enter")
page_b.get_by_label("Location").press("Enter")
browser.close()
playwright_.stop()
