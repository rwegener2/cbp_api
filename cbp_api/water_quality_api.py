import os
from datetime import datetime, date, timedelta
from typing import List, Dict

import pandas as pd
from pandas._libs.tslibs.parsing import DateParseError

from cbp_api.models import Result, Station
from cbp_api.cbp_base_api import CBPBaseApi


class WaterQualityApi(CBPBaseApi):
    def __init__(self):
        super().__init__()
        self._api_endpoint = 'WaterQuality'
        self._data_vars_dict = {}
        self._program_codes, self.programs = self._retrieve_programs()
        self._variable_codes, self.data_variables = self._retrieve_substances()

    def _retrieve_programs(self):  # TODO how to do typing with tuple result
        """
        Ping the Programs endpoint and create a dictionary containing available project
        codes and their identifying strings
        """
        return self._retrieve_endpoint('WaterQuality/Programs', 'ProgramIdentifier', 'ProgramId')

    def get_station(self, geo_attr: str, geo_id: str) -> Station:
        """
        Get first station (maybe this would be more useful if it got a station by ID) ->
        this api endpoint doesnt give id, just name :grimmace:
        """
        path = os.path.join('Station', geo_attr, geo_id)
        result = self._rest_adapter.get(endpoint=path)
        station_info = Station(**result.data[0])
        return station_info

    def get_stations(self,  geo_attr: str, geo_id: str) -> pd.DataFrame:
        """
        Get list of all stations

        params:
        - geography type (ex. huc8, fips, coordinates) "geographic attribute" Possible values are:
        HUC8, HUC12, CBSeg2003, CBSegmentShed2009, FIPS, State, CountyCity
        Implemented: 
        - geography id (ex. 2, AJFDK, [32, 12]) -- accepts a list of HUCs, etc. "geographic id"
        """
        if geo_attr not in ['HUC8']:
            raise Exception('geo_attr', geo_attr, "not supported. Please choose from ['HUC8']")
        # TODO lots more checks on validitiy of inputs
        
        path = os.path.join(self._api_endpoint, 'Station', geo_attr, geo_id)
        result = self._rest_adapter.get(endpoint=path)
        stations_list = []
        for station in result.data:
            # stations_list.append(Station(**station))
            stations_list.append(station)
        return pd.DataFrame(stations_list)

    def get_from_endpoint(self, endpoint: str) -> Result:
        result = self._rest_adapter.get(endpoint=endpoint)
        return result

    def get_measurements(
            self, 
            geog_attr: str = 'HUC8',
            geog_id: str | int | List[str] = 'all',  # TODO accept multiple inputs
            start_date: str | datetime | date = date.today() - timedelta(days=365), 
            end_date: str | datetime | date = date.today(),
            data_variables: str | List[str] = 'WTEMP',  # TODO accept multiple inputs
            data_stream: str = 'traditional',
            program: str = 'all',
            ) -> pd.DataFrame:

        # Check geography type and create list of corresponding codes
        if geog_attr not in ['HUC8']:
            raise KeyError('geog_attr not yet supported. Please use HUC8')

        if geog_id == 'all':
            geog_id = self._huc8_codes.values()
        else:
            geog_id = self._huc8_codes[geog_id]
        
        # TODO Should be using actual HUC8 codes, not the CBay identifiers
        # Ex. '02040205' not '1'
        # geog_id_formatted = self._create_string_from_list(geog_id)

        # Ensure start and end date inputs are in proper string format
        start_date = self._parse_date(start_date)
        end_date = self._parse_date(end_date)

        # Extract data variable (substance) code
        try:
            data_var_id = self._variable_codes[data_variables]
        except KeyError:
            raise KeyError('Invalid entry for argument data_variables. Valid inputs are',
                self._variable_codes.keys(), '. See self.data_variables for details.')

        # TODO figure out what this is and update accordingly
        project_id = '12,13,15,35,36,2,3,7,33,34,23,24'

        # check inputs
        if data_stream == 'traditional':
            data_stream_id = '0'
        elif data_stream == 'non-traditional':
            data_stream_id = '1'
        elif data_stream == 'both':
            data_stream_id = '0,1'
        else:
            raise KeyError("Invalid entry for argument data_stream. Must be either \
                           'traditional', 'non-traditional', or 'both.")

        # Extract program code
        if program == 'all':
            program_id = self._create_string_from_list(self._program_codes.values())
        else:
            try:
                program_id = self._program_codes[program]
            except KeyError:
                raise KeyError('Invalid entry for argument program. Valid inputs are',
                               self._program_codes.keys(), '. See self.programs for details.')

        # build endpoint
        endpoint = f'{self._api_endpoint}/WaterQuality/{start_date}/{end_date}/{data_stream_id}/{program_id}/{project_id}/{geog_attr}/{geog_id_formatted}/{data_var_id}'
        result = self._rest_adapter.get(endpoint=endpoint)
        return pd.DataFrame(result.data)

    def list_datavariables(self) -> pd.DataFrame:
        """
        Returns a pandas dataframe of the available variables and their associated
        string name for use in the `get_measurements()` method.
        """
        raise NotImplementedError
    
    @staticmethod
    def _create_string_from_list(l: str | int | List) -> str:
        """
        Creates a string from a list by converting list elements to strings. List elements
        are comma-seperated.
        Ex. input: [3, 901, 7] -> output: '3,901,7'
        """
        if isinstance(l, int):
            l = str(l)
        return ','.join(map(str, list(l)))

    @staticmethod
    def _parse_date(date_input: str | datetime | date) -> str:
        if isinstance(date_input, str):
            try:
                # TODO why go to pandas and back to a string? Check first if string is
                # in the desired format.
                date_input = pd.to_datetime(date_input)
            except DateParseError:
                raise('Could not parse the date using pd.to_datetime(). Please provide \
                      date string in mm-dd-yyyy format.')
        date_input = date_input.strftime('%m-%d-%Y') 
        return date_input


'WaterQuality/WaterQuality/11-24-2022/12-21-2024/0/2,4,6/12,13,15,35,36,2,3,7,33,34,23,24/HUC8/4,6,8/123'
'WaterQuality/WaterQuality/2022-11-24 00:00:00/2024-12-21/0/2,4,6/12,13,15,35,36,2,3,7,33,34,23,24/HUC8/4,6,8/123'
