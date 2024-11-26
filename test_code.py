# REST ADAPTER

# from cpb_api.rest_adapter import RestAdapter

# api = RestAdapter(hostname='datahub.chesapeakebay.net/api.json/WaterQuality/')
# out = api.get('Station/HUC8/3')
# out = api.get('WaterQuality/6-29-2010/6-29-2015/0,1/2/12/HUC8/20/23')

# Example API Calls:
# Station
# https://datahub.chesapeakebay.net/api.JSON/WaterQuality/Station/HUC8/3

# Water Quality
# http://datahub.chesapeakebay.net/api.JSON/WaterQuality/WaterQuality/6-29-2010/6-29-2015/0,1/2/12/HUC8/20/23
# Get WQ data from all programs (just include comma seperate numbers)
# https://datahub.chesapeakebay.net/api.JSON/WaterQuality/WaterQuality/6-29-2010/6-29-2015/0,1/2,4,6/12/HUC8/20/23

# WATER QUALITY API

from datetime import datetime, date
from cbp_api.water_quality_api import WaterQualityApi

api = WaterQualityApi()

# out = api.get_measurements(geog_id = '4', start_date='11-24-2022', program='all', data_variables= 'ZN')

out = api.get_measurements(geog_id = [4, 6, 8], start_date='11-24-2022', program='all')

out = api.get_measurements(geog_id = 'all', start_date='11-24-2022', program='all')

# out = api.get_measurements(geog_id = '4', end_date=datetime.now(), start_date = '11-23-2022', program='all')
# out = api.get_measurements(geog_id = '4', end_date=date.today(), program='all')


# # out = api.get('Station/HUC8/3')
# # out = api.get_measurement()
# # station = api.get_station('Station/HUC8/3')
# # station_list = api.get_stations(geo_attr= 'HUC8', geo_id = '3')
# station_list = api.get_stations(geo_attr= 'CBSegmentShed2009', geo_id = 'CB1TF')
# Not sure why but https://datahub.chesapeakebay.net/api.json/WaterQuality/Station/CBSegmentShed2009/CB1TF errors



# station_list = api.get_stations('Station/HUC8/3')

# mulitple_hucs = api.get_stations('Station/HUC8/2,4,6')

# from cpb_api.cbp_base_api import CBPBaseApi

# api = CBPBaseApi()
# # huc8_result = api.get_huc8s()
# state_results = api.get_states()
