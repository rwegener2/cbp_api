Start with: Water Quality Endpoint

Rest API building reference: https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/


## Stations
realistically, people want to: 
- view a list of stations by geographic region (including all stations) as pandas / geopandas dataframe (?)
- search for the nearest stations to a point (dependent on generating a list of all the stations)
- view located stations on a map

Stations API gives list of stations. Includes a myriad of geographic descriptors. Most useful ones are probably city/state and lat/lon. Map display may also be nice (maybe just a wrapper around the geopandas .explore() method?)

Steps:
1. Set up the `get_stations()` method to return a pandas dataframe
2. Remove string literals from `get_stations()` arguments AKA implement search parameters for the named geographic units
2. Figure out how to search for all the stations and return a df
3. Search radius method? (or save for later and move onto a data endpoint)

Pausing on Stations for now since it seems like that endpoint isn't actually very useful... :,(

## WaterQuality

MVP of waterquality endpoint works!!!
Next steps: flesh out the underlying functionality behind the input arguments
- biggest thing: develop some kind of system to build dictionaries of data variables / partner programs (/ more?) that can be more quickly referenced when building the query
- connected to that is more checking of input argument values
- then... maybe start writing some tests to confirm functionality works under a variety of circumstances ?!?

Pre-Github:
- figure out a simple default for projects (all?)
- make data vars accept a list of vars

### Getting all the stations in one request

Trying to identify the geographic attribute type with the fewest categories.

*HUC8 - 80
*HUC12 - (this must be more than HUC8 zones)
*CBSeg2003 - 
Station - 
EcoRegion - 
Facility - 
State - 7
CBPBasin - 
*City/County (FIPS)
*SegmentShed2009 - 112
*Monitoring Station

* = apparently you can only filter WaterQuality calls by these geographic attributes :/
