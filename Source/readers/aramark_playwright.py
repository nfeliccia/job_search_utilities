from playwright.sync_api import Page
from playwright.sync_api import Playwright, sync_playwright


def select_corporate_id(sci_page: Page = None):
    sci_page.locator("label").filter(has_text="Corporate & Field Support").get_by_label("checkmark").click()
    sci_page.locator("label").filter(has_text="Information Technology").get_by_label("checkmark").click()


def aramark(playwright: Playwright, qth: str, keyword_list: list[str]) -> None:
    """

    Args:
        playwright: A playwright object.
        qth: location for search
        keyword_list: list of keywords to search for

    Returns:

    """
    # ---------------------
    # Test case scenario
    # ---------------------
    # Open Aramark Website.
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1280, 'height': 720})
    page = context.new_page()
    where_ = "Where?"
    what_ = "What?"
    sb = "searchbox"
    target_website = "https://careers.aramark.com/search/"

    page.goto(target_website)
    page.locator("#onetrust-close-btn-container").get_by_label("Close").click()
    page.get_by_test_id("widget_chatbox_popover").get_by_label("Close").click()

    pages = [context.new_page() for _ in range(len(keyword_list))]
    for i, keyword in enumerate(keyword_list):
        pages[i].goto(target_website)
        pages[i].get_by_role(sb, name=what_).click()
        pages[i].get_by_role(sb, name=what_).fill(keyword)
        pages[i].get_by_role(sb, name=where_).click()
        pages[i].get_by_role(sb, name=where_).fill(qth)

    # New Page
    page2 = context.new_page()
    page2.goto(target_website)
    select_corporate_id(page2)
    page2.get_by_role("button", name="Load More").click()
    page2.get_by_label("Location").click()
    page2.get_by_label("Location").fill(qth)
    page2.locator("label").filter(has_text="Salaried").get_by_label("checkmark").click()

    input("press anykey to close")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    qth = '19124'
    kl = ["Python", "Data Science", "Machine Learning", "Data Analyst", "Data Engineer", "Data Scientist"]
    aramark(playwright=playwright, qth=qth, keyword_list=kl)
