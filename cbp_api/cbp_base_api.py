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
        self._huc8s = None
        self._data_variables = None
        self._data_streams = None
    
    @property
    def huc8s(self):
        if self._huc8s is None:
            huc8s = self._retrieve_endpoint('HUC8', 'HUC8Id')
            huc8s.rename(columns={'HUC8Code': 'HUC8String',
                                  'HUC8Name': 'HUC8Description'},
                        inplace=True)
            self._huc8s = huc8s
        return self._huc8s

    @property
    def data_streams(self):
        if self._data_streams is None:
            data_streams = self._retrieve_endpoint('DataStreams', 'Value')
            data_streams.index.rename('DataStreamId', inplace=True)
            # Add empty column for kwarg string
            data_streams.insert(0, 'DataStreamString', None)
            # Set identifer names
            data_streams.at['0,1', 'DataStreamString'] = 'all'
            data_streams.at['1', 'DataStreamString'] = 'non-traditional'
            data_streams.at['0', 'DataStreamString'] = 'traditional'
            # Rename description column
            data_streams.rename(columns={'DataStreamName': 'DataStreamDescription'},
                                inplace=True)
            # Assign to property
            self._data_streams = data_streams
        return self._data_streams
    
    @property
    def data_variables(self):
        """
        Ping the Substances endpoint and create a dictionary containing available project
        codes and their identifying strings
        """
        if self._data_variables is None:
            data_variables = self._retrieve_endpoint('Substances', 'SubstanceId')
            self._data_variables = data_variables
            data_variables.rename(columns=
                                {'SubstanceIdentificationName': 'DataVariableString', 
                        'SubstanceIdentificationDescription': 'DataVariableDescription'
                        },
                inplace=True,
                )
        return self._data_variables
    
    # def _build_results_lists(self, endpoint: str, model):
    #     results = self._rest_adapter.get(endpoint=endpoint)
    #     results_list = []
    #     for result in results_list.data:
    #         results_list.append(model(**result))
    #     return results_list
    
    # def get_huc8s(self) -> List[HUC8]:
    #     huc8_results = self._rest_adapter.get(endpoint='HUC8')
    #     huc8_list = []
    #     for huc8 in huc8_results.data:
    #         huc8_list.append(HUC8(**huc8))
    #     return huc8_list

    # def get_states(self) -> List[State]:
    #     state_results = self._rest_adapter.get(endpoint='State')
    #     state_list = []
    #     for state in state_results.data:
    #         state_list.append(State(**state))
    #     return state_list
    
    def _retrieve_endpoint(self, endpoint: str, id_key: str) -> pd.DataFrame:
        """
        Send a get request to the specified endpoint and return a dictionary containing
        the names of the parameters of interest and the ids used to identify them in the
        API search calls.
        endpoint - endpoint url to ping
        id_key - data response to use to set the index of the dataframe of response data
        """
        results = self._rest_adapter.get(endpoint)
        # create dict of program codes
        # codes = {}
        # for var in results.data:
        #     codes[var[name_key]] = var[id_key]
        # create data frame for users
        df = pd.DataFrame(results.data)
        df = df.set_index(id_key)
        if df.index.has_duplicates:
            raise Exception('API call returned non-unique ids')
        return df
