from typing import List, Dict

class Result:
    def __init__(self, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []

class Station:
    """
    Station information as returned from the WaterQuality/Station endpoint
    """
    def __init__(self, Station: str, StationDescription: str, CBSeg2003: str, 
                 CBSeg2003Description: str, CBSegmentShed2009: str, CBSegmentShed2009Description: str,
                 HUC8: str, HUC12: str, FIPS: str, State: str, CountyCity: str, USGSGage: str, 
                 FallLine: str, Latitude: str, Longitude: str, UTMX: int, UTMY: int, LLDatum: str,
                 ):
        self.station = Station
        self.station_description = StationDescription
        self.cb_seg2003 = CBSeg2003
        self.cb_seg2003_description = CBSeg2003Description
        self.cb_segment_shed2009 = CBSegmentShed2009
        self.cb_segment_shed2009_description = CBSegmentShed2009Description
        self.huc8 = HUC8
        self.huc12 = HUC12
        self.fips = FIPS
        self.state = State
        self.county_city = CountyCity
        self.usgs_gage = USGSGage
        self.fall_line = FallLine
        self.latitude = Latitude
        self.longitude = Longitude
        self.utmx = UTMX
        self.utmy = UTMY
        self.ll_datum = LLDatum

class HUC8:
    def __init__(self, HUC8Id: int, HUC8Code: str, HUC8Name: str):
        self.huc8_id = HUC8Id
        self.huc8_code = HUC8Code
        self.huc8_name = HUC8Name
    
    def __repr__(self):
        repr_dict = {
            'huc8_id': self.huc8_id, 'huc8_code': self.huc8_code, 'huc8_name': self.huc8_name
            }
        return "cpb_api.models.HUC8: " + str(repr_dict)

class State:
    def __init__(self, State: str, Name: str):
        self.state = State
        self.name = Name

    def __repr__(self):
        repr_dict = {'state': self.state, 'name': self.name}
        return "cpb_api.models.State: " + str(repr_dict)
