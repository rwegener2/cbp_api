import requests
from typing import List, Dict

from cbp_api.models import Result
from cbp_api.exceptions import CPBException


class RestAdapter:
    """
    Class that translates a generic REST API endpoint into a Python requests library call
    """
    def __init__(self, hostname: str, ssl_verify: bool = True):
        self.url = f"https://{hostname}/"
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def get(self, endpoint: str) -> Result:
        full_url = self.url + endpoint
        headers = {}
        try:
            response = requests.get(url=full_url, verify=self._ssl_verify, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise CPBException("Request failed. Endpoint url:", full_url) from e
        data_out = response.json()
        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        if is_success:
            return Result(response.status_code, message=response.reason, data=data_out)
        raise CPBException(f"{response.status_code}: {response.reason}")
