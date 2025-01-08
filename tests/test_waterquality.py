import pytest
from datetime import date, datetime

import pandas as pd
from pandas._libs.tslibs.parsing import DateParseError

from cbp_api.water_quality_api import WaterQualityApi
from cbp_api.models import MeasurementDataFrame

@pytest.fixture
def api():
    return WaterQualityApi()

def test_get_measurements_defaults(api):
    out_df = api.get_measurements()

    assert isinstance(out_df, pd.DataFrame)

@pytest.mark.parametrize('start_date', 
                         ['11-24-2023', '2023-06-30', date(2023, 11, 15), datetime(2023, 10, 23)])
@pytest.mark.parametrize('end_date', 
                         ['12-31-2023', '2023-12-31', date(2023, 12, 31), datetime(2023, 12, 31)])
@pytest.mark.parametrize('data_variables', ['SALINITY', ['SALINITY', 'TSS']])
@pytest.mark.parametrize('geog_ids', ['02060001', ['02060001', '02070011']])
@pytest.mark.parametrize('data_streams', ['both'])
@pytest.mark.parametrize('programs', ['TWQM', ['TWQM', 'SWM']])
def test_get_measurements(api, start_date, end_date, data_variables, geog_ids, data_streams, programs):
    out_df = api.get_measurements(
        geog_ids=geog_ids,
        start_date=start_date,
        end_date=end_date,
        data_variables=data_variables, 
        data_streams=data_streams,
        programs=programs,
        )

    # TODO left off -- why am I getting an ambiguous error when running the schema.validate()
    # here? I'm not getting it when validating in the notebook >:(
    assert isinstance(out_df, pd.DataFrame)
    assert MeasurementDataFrame.validate(out_df)

def test_error_get_measurements_start_date(api):
    with pytest.raises(DateParseError) as e_info:
        api.get_measurements(start_date='01012012')

    # assert e_info.value.args[0] == 'some info'
# TODO test more invalid inputs (ex. geog id isn't valid)

# TODO test error on a call with no results
