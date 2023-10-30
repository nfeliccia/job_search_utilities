import logging

from readers_common_old import GeneralReader


class HealthverityReader(GeneralReader):

    def __init__(self):
        super().__init__()  # Initialize the parent class

    def read_jobs(self, testmode=False):
        # Define the URL
        careers_url = "https://healthverity.com/careers/opportunities/"

        try:
            # Open the careers page
            self.open_a_tab(careers_url)
        except Exception as e:
            logging.error(f"An error occurred while opening the Healthverity careers page: {e}", exc_info=True)

        self.close_with_test(testmode=testmode)


# The script can be run as a standalone script or imported as a module
if __name__ == "__main__":
    with HealthverityReader() as reader:
        reader.read_jobs(testmode=False)
