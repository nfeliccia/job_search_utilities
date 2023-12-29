from Source import GeneralReaderPlaywright


class SystemOneReader(GeneralReaderPlaywright):
    # Set base URL and static path/hash components
    BASE_URL = "https://jobs.systemone.com/"
    PATH = "l/recruiting/jobsearchaction/b440eda6-9cc2-11e4-a7c5-bc764e10782d"
    STATIC_HASH = "f40610d2-abe2-11ed-9711-42010a8a0fd9"  # This is the static hash we're reusing
    FULL_BASE_URL = f"{BASE_URL}{PATH}/{STATIC_HASH}/false"
    company_name = "systemone"

    SYSTEMONE_PARAMETERS = [
        {"sortBy": "beginTime", "term": '"Data Science"', "title": "", "postalCode": ""},
        {"sortBy": "beginTime", "term": '"Machine Learning"', "title": "", "postalCode": ""},
        {"sortBy": "beginTime", "term": '"Python"', "title": "", "postalCode": ""},
        {"sortBy": "beginTime", "term": '"Data Science"', "title": "", "postalCode": "19124"},
        {"sortBy": "beginTime", "term": '"Machine Learning"', "title": "", "postalCode": "19124"},
        {"sortBy": "beginTime", "term": '"Python"', "title": "", "postalCode": "19124"}
    ]

    def __init__(self, testmode: bool = False, customer_id: str = None, base_url: str = None)
        super().__init__(root_website=self.BASE_URL, company_name=self.company_name, testmode=testmode,
                         customer_id=customer_id)
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = FULL_BASE_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = SYSTEMONE_PARAMETERS


if __name__ == "__main__":
    with SystemOneReader() as sor:
        sor.open_job_pages(base_url=sor.base_url, parameters=sor.parameters)
        print(sor.webdriver.title)
        sor.close_with_test(testmode=False)
