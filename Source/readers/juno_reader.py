from Source import GeneralReaderPlaywright


class JunoReader(GeneralReaderPlaywright):
    company_name = "juno"
    jobs_website = "https://www.junosearchpartners.com/work"

    def __init__(self, customer_id: str = None, testmode: bool = False):
        super().__init__(root_website=self.jobs_website, company_name=self.company_name, testmode=testmode,
                         customer_id=customer_id)

    def do_juno(self):
        """
        Juno is just a list ; I tried to filter with no success. This opens it up and closes the pop up if available.
        Returns:

        """
        page = self.create_new_tab()
        # First handle the cookies.
        page.get_by_label("Close").click()
        self.close_with_test()


if __name__ == "__main__":
    nic_ = "nic@secretsmokestack.com"
    JunoReader(customer_id=nic_).do_juno()
