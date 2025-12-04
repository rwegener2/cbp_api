This api call doesn't work:
https://datahub.chesapeakebay.net/api.json/WaterQuality/WaterQuality/01-01-2023/01-01-2024/0/6/12,13,15,35,36,2,3,7,33,34,23,24/HUC8/2/
or:
```
out = api.get_measurements(geog_type='HUC8', geog_id='02050101', start_date='2023-01-01',
                           end_date='2024-01-01', data_variables='CHL_A', data_stream='traditional',
                           program='TWQM')
```
When you go in and put these parameters in the GUI the HUC8 zone '02050101' doesn't exist. So maybe it isn't an option? But is there a way to know what the options would be?

This api call does work:
https://datahub.chesapeakebay.net/api.json/WaterQuality/WaterQuality/01-01-2023/01-01-2024/0/2,4,6/12,13,15,35,36,2,3,7,33,34,23,24/HUC8/2/
```
out = api.get_measurements(geog_type='HUC8', geog_id='02050101', start_date='2023-01-01',
                           end_date='2024-01-01', data_variables='CHL_A', data_stream='traditional',
                           program='all')
```
But it's a bit hard to follow because chlorophyll-a isn't an available parameter for any of the stations in this date/location range. This is navicable in the API (becuase you won't be allowed to select CHL_A) but you have to play with it in the API version.
