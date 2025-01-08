import os
from datetime import datetime, date, timedelta
from typing import List

import pandas as pd
from pandera.typing import DataFrame
from pandas._libs.tslibs.parsing import DateParseError

from cbp_api.models import Result, MeasurementDict, MeasurementDataFrame
from cbp_api.cbp_base_api import CBPBaseApi


class WaterQualityApi(CBPBaseApi):
    def __init__(self):
        super().__init__()
        self._api_endpoint = 'WaterQuality'
        self._programs = None

    @property
    def geog_types(self):
        """
        Geography types currently supported by this package
        """
        return pd.DataFrame(
            {
                'GeogTypeString': ['HUC8'], 
                'GeogTypeDescription': 
                ['USGS Hydrologic unit subbasin codes https://nas.er.usgs.gov/hucs.aspx'], 
                }
            )

    @property
    def programs(self):
        """
        Ping the Programs endpoint and create a dictionary containing available project
        codes and their identifying strings
        """
        if self._programs is None:
            programs = self._retrieve_endpoint('WaterQuality/Programs', 'ProgramId')
            programs.rename(columns={'ProgramIdentifier': 'ProgramString',
                                    'ProgramName': 'ProgramDescription'},
                                    inplace=True)
            self._programs = programs
        return self._programs 

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
                date_input = pd.to_datetime(date_input)
            except DateParseError:
                raise DateParseError('Could not parse the date using pd.to_datetime(). Please provide \
                      date string in mm-dd-yyyy format.')
        date_input = date_input.strftime('%m-%d-%Y') 
        return date_input

    def get_from_endpoint(self, endpoint: str) -> Result:
        result = self._rest_adapter.get(endpoint=endpoint)
        return result
    
    def get_measurements(
            self, 
            geog_type: str = 'HUC8',
            geog_ids: str | int | List[str] = 'all',
            start_date: str | datetime | date = date.today() - timedelta(days=365), 
            end_date: str | datetime | date = date.today(),
            data_variables: str | List[str] = 'WTEMP',
            data_streams: str = 'traditional',
            programs: str | List[str] = 'all',
            ) -> MeasurementDataFrame:
        """
        data_variables the Substance Identification Name for one or more measurement variables
        geog_type - 'HUC8' is only form of geospatial filtering currently supported. Use
        'all' to get data from all HUC8 zones
        data_variables - use WaterQualityApi.data_variables to see list of options and 
        Indentification Names
        data_stream -
        program - use WaterQualityApi.programs to see a list of options. Use Program Identifier
        as input
        """
        out = pd.DataFrame(self._get_waterquality_data(geog_type, geog_ids, start_date, end_date,
                                                data_variables, data_streams, programs))
        if out.empty is True:
            print('Search was too narrow and did not return any results. Output dataframe' \
                  'will be empty.')
        else:
            out['SampleDateTime'] = pd.to_datetime(out['SampleDate'] + out['SampleTime'], format='%Y-%m-%dT00:00:00%H:%M:%S')
            out = out.drop(columns=['SampleDate', 'SampleTime'])
            out = out.sort_values(['SampleDateTime', 'Station'])
            out = out.set_index(['SampleDateTime'])
        return out
    
    def _get_waterquality_data(
            self,
            geog_type: str = 'HUC8',
            geog_ids: str | List[str] = 'all',
            start_date: str | datetime | date = date.today() - timedelta(days=365), 
            end_date: str | datetime | date = date.today(),
            data_variables: str | List[str] = 'WTEMP',
            data_streams: str = 'traditional',
            programs: str | List[str] = 'all',
            ) -> List[MeasurementDict]:

        # Check geography type and create list of corresponding codes
        if geog_type not in ['HUC8']:
            raise KeyError("geog_type not yet supported. Please use geog_type='HUC8'")

        if geog_ids == 'all':
            geog_id_string = self._create_string_from_list(self.huc8s.index)
        else:
            try:
                if isinstance(geog_ids, str):
                    geog_ids = [geog_ids]
                geog_id_list = self.huc8s[self.huc8s['HUC8String']
                                                .isin(geog_ids)].index
                if len(geog_id_list) == 0:
                    raise Exception('Geog ids not found in available huc8 zones. Please see' /
                                    'WaterQualityApi.huc8s.HUC8String.values for available inputs.')
                geog_id_string = self._create_string_from_list(geog_id_list)
            except KeyError:
                raise KeyError('Invalid entry for argument geog_id. Valid inputs are',
                               self.huc8s.index, '. See WaterQualityApi.huc8s for details.')
        
        # Ensure start and end date inputs are in proper string format
        start_date = self._parse_date(start_date)
        end_date = self._parse_date(end_date)

        # Extract data variable (substance) code
        try:
            if isinstance(data_variables, str):
                data_variables = [data_variables]
            data_var_ids = self.data_variables[self.data_variables['DataVariableString']
                                      .isin(data_variables)].index
            data_var_string = self._create_string_from_list(data_var_ids)
        except KeyError:
            raise KeyError('Invalid entry for argument data_variables. Valid inputs are',
                self.data_variables, '. See WaterQualityApi.data_variables for details.')

        # TODO figure out what this is and update accordingly
        project_id = '12,13,15,35,36,2,3,7,33,34,23,24'

        # check inputs
        if data_streams == 'traditional':
            data_stream_id = '0'
        elif data_streams == 'non-traditional':
            data_stream_id = '1'
        elif data_streams == 'both':
            data_stream_id = '0,1'
        else:
            raise KeyError("Invalid entry for argument data_stream. Must be either \
                           'traditional', 'non-traditional', or 'both.")

        # Extract program code
        if programs == 'all':
            program_ids = self._create_string_from_list(self.programs.index)
        else:
            try:
                if isinstance(programs, str):
                    programs = [programs]
                program_id_list = self.programs[self.programs['ProgramString']
                                                .isin(programs)].index
                program_ids = self._create_string_from_list(program_id_list)
            except KeyError:
                raise KeyError('Invalid entry for argument program. Valid inputs are',
                               self.programs.index, '. See WaterQualityApi.programs for details.')

        # build endpoint
        endpoint = f'{self._api_endpoint}/WaterQuality/{start_date}/{end_date}/{data_stream_id}/{program_ids}/{project_id}/{geog_type}/{geog_id_string}/{data_var_string}'
        result = self._rest_adapter.get(endpoint=endpoint)
        return result.data

    def get_stations(self,  geo_attr: str, geo_id: str) -> pd.DataFrame:
        """
        Get list of all stations within a certain geography. Returns all the station's
        geography attributes (nothing about variables, dates of measurement, or other science
        data, though)

        params:
        - geography type (ex. huc8, fips, coordinates) "geographic attribute" Possible values are:
        HUC8, HUC12, CBSeg2003, CBSegmentShed2009, FIPS, State, CountyCity
        Implemented: 
        - geography id (ex. 2, AJFDK, [32, 12]) -- accepts a list of HUCs, etc. "geographic id"
        """
        raise NotImplementedError
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
