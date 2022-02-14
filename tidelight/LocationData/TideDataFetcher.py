import logging

from kartverket_tide_api import TideApi
from kartverket_tide_api.parsers import LocationDataParser

from tidelight.LocationData.Location import Location
from tidelight.util import get_next_time_from, get_next_time_to


class TideDataFetcher:
    api = TideApi()

    def __init__(self, location: Location):
        self.lat = location.lat
        self.lon = location.lon

    def fetch(self, from_time, to_time):
        response = self.api.get_location_data(self.lon, self.lat, from_time,
                                              to_time, 'TAB')
        if self.valid_xml(response):
            return response
        return None

    @staticmethod
    def valid_xml(xml_string: str):
        parser = LocationDataParser(xml_string)
        try:
            water_levels = parser.parse_response()['data']
            if water_levels is not None:
                if len(water_levels) != 0:
                    return True
        except Exception as e:
            return False
        return False
