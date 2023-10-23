from readers_common import GeneralReader

CUBESMART_URL = "https://careers.cubesmart.com/careers-home/jobs"
CUBESMART_PARAMETERS = [
    {'keywords': 'Data', 'sortBy': 'relevance', 'page': '1', 'lat': '40.0326656', 'lng': '-75.0616576',
     'radiusUnit': 'MILES', 'radius': '25', 'view': 'search'}]


class CubeSmartReader(GeneralReader):

    def __init__(self, base_url: str = None, parameters: list = None, testmode: bool = False):
        super().__init__()
        self.testmode = testmode

        # Loadable Base URL
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = CUBESMART_URL

        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = CUBESMART_PARAMETERS

    def read_jobs(self):
        # Open the careers page with the specified parameters
        self.open_job_pages(self.base_url, self.parameters)


# The script can be run as a standalone script or imported as a module
if __name__ == "__main__":
    with CubeSmartReader(testmode=False) as reader:
        reader.read_jobs()
        reader.close_with_test(testmode=reader.testmode)
