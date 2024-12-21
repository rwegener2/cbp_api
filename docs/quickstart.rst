CBP_API Quickstart
==================

The Chesapeake Bay Program Datahub has APIs for a variety of data variables. At this point in 
development this Python package supports the `WaterQuality API <https://datahub.chesapeakebay.net/api#waterquality>`_.

To access this module, first import it and initialize the API object.

.. code-block:: python

   from cpb_api.water_quality_api import WaterQualityApi

    api = WaterQualityApi()

The API object can be used to search for data.

.. code-block:: python

    data = api.get_measurements(
        geog_id = [4, 6, 8], 
        start_date='11-24-2022', 
        program='all'
    )

The :code:`.get_measurements()` method returns a pandas dataframe of results.

By default :code:`.get_measurements()` will return ... 

See this other link (TBD) for a more detailed description of the search parameters.
