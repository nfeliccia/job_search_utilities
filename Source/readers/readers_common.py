from playwright.sync_api import sync_playwright


class GeneralReaderPlaywright:

    def __enter__(self):
        return self  # this is the object that will be bound to the variable in the `with` statement

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()  # clean up resources here

    def __init__(self, root_website: str = None, testmode: bool = False):
        self.testmode = testmode
        self.root_website = root_website
        self.playwright = None
        self.browser = None
        self.context = None
        self.setup_playwright()

    def setup_playwright(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)  # headless=False if testmode=True
        self.context = self.browser.new_context(viewport={'width': 1280, 'height': 720})

    def create_new_tab(self, website: str = None):
        if website is None:
            website = self.root_website
        page = self.context.new_page()
        page.goto(website)
        return page

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
