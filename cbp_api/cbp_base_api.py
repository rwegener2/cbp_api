from typing import List

import pandas as pd

from cbp_api.rest_adapter import RestAdapter
from cbp_api.models import Result, HUC8, State

_BASE_URL = 'datahub.chesapeakebay.net/api.json'

class CBPBaseApi():
    """
    REST API adapter for endpoints following datahub.chesapeakebay.net/api.json
    Implemented: HUC8
    Error Result: FIPS, SegmentShed2009
    """
    def __init__(self):
        self._rest_adapter = RestAdapter(_BASE_URL)
        self._huc8_codes, self.huc8s = self._retrieve_huc8s()
    
    # def _build_results_lists(self, endpoint: str, model):
    #     results = self._rest_adapter.get(endpoint=endpoint)
    #     results_list = []
    #     for result in results_list.data:
    #         results_list.append(model(**result))
    #     return results_list
    
    def get_huc8s(self) -> List[HUC8]:
        huc8_results = self._rest_adapter.get(endpoint='HUC8')
        huc8_list = []
        for huc8 in huc8_results.data:
            huc8_list.append(HUC8(**huc8))
        return huc8_list

    def get_states(self) -> List[State]:
        state_results = self._rest_adapter.get(endpoint='State')
        state_list = []
        for state in state_results.data:
            state_list.append(State(**state))
        return state_list
    
    def _retrieve_endpoint(self, endpoint: str, name_key: str, id_key: str):
        results = self._rest_adapter.get(endpoint)
        # create dict of program codes
        codes = {}
        for var in results.data:
            codes[var[name_key]] = var[id_key]
        # create data frame for users
        df = pd.DataFrame(results.data)
        return codes, df       
    
    def _retrieve_substances(self):  # TODO how to do typing with tuple result
        """
        Ping the Substances endpoint and create a dictionary containing available project
        codes and their identifying strings
        """
        return self._retrieve_endpoint('Substances', 'SubstanceIdentificationName', 'SubstanceId')

    def _retrieve_huc8s(self):
        return self._retrieve_endpoint('HUC8', 'HUC8Code', 'HUC8Id')
