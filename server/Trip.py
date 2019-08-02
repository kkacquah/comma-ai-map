import json
import datetime
import pandas as pd

ISO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
DECIMAL_PLACES_TO_ROUND = 2
TRIP_SAMPLE_RATE = 15

class Trip(object):

    def __init__(self, file):
        # Trip is a list of dictionaries with the following format
        # {"lat": 37.25585893874121,
        # "speed": 26.30250495735354,
        # "lng": -122.41407280418797,
        # "dist": 7.1663417633771935,
        # "index": 486}

        # start_time and end_time are the beginning and the end of the trip
        self._coordinate_dataframe, self._start_time, self._end_time = self._read_trip_info_from_file(file)

    def _read_trip_info_from_file(self, file):
        comma_ai_trip = json.load(file)
        start_time_str = comma_ai_trip['start_time']
        end_time_str = comma_ai_trip['end_time']
        commma_ai_coordinate_list = comma_ai_trip['coords']
        coordinates_dataframe = self._get_coordinate_dataframe_from_commma_ai_coordinate_list(commma_ai_coordinate_list)
        start_time = datetime.datetime.strptime(start_time_str, ISO_DATE_FORMAT)
        end_time = datetime.datetime.strptime(end_time_str, ISO_DATE_FORMAT)
        return coordinates_dataframe, start_time, end_time

    def _truncate_lng_and_lat(self, series_to_truncate):
        series_to_truncate['lat'] = round(series_to_truncate['lat'], DECIMAL_PLACES_TO_ROUND)
        series_to_truncate['lng'] = round(series_to_truncate['lng'], DECIMAL_PLACES_TO_ROUND)
        return series_to_truncate

    def _get_series_from_comma_ai_coordinate(self, commma_ai_coordinate):
        commma_ai_coordinate = commma_ai_coordinate
        coordinate_series = pd.Series(data = commma_ai_coordinate)
        coordinate_series = self._truncate_lng_and_lat(coordinate_series)
        return coordinate_series

    def _get_coordinate_dataframe_from_commma_ai_coordinate_list(self,commma_ai_coordinate_list):
        coordinates_dataframe = pd.DataFrame()
        #populate initial entry so it has a speed
        coordinate_series = self._get_series_from_comma_ai_coordinate(commma_ai_coordinate_list[0])
        coordinate_series['prev_lat'] = coordinate_series['lat']
        coordinate_series['prev_lng'] = coordinate_series['lng']
        #For keeping track of previous lat and lng for loop.
        prev_lat = coordinate_series['lat']
        prev_lng = coordinate_series['lng']
        #insert first entry into dataframe
        coordinates_dataframe.insert(0,0,coordinate_series, allow_duplicates = False)
        #Start so every series has a prev long and lat

        for i in range(TRIP_SAMPLE_RATE,len(commma_ai_coordinate_list),TRIP_SAMPLE_RATE):
            coordinate_series = self._get_series_from_comma_ai_coordinate(commma_ai_coordinate_list[i])
            #add previous values to coordinate series
            coordinate_series['prev_lat'] = prev_lat
            coordinate_series['prev_lng'] = prev_lng
            prev_lat = coordinate_series['lat']
            prev_lng = coordinate_series['lng']
            index = i//TRIP_SAMPLE_RATE
            coordinates_dataframe.insert(index,index,coordinate_series, allow_duplicates = False)
        coordinates_dataframe = coordinates_dataframe.transpose()
        return coordinates_dataframe


    def get_coordinate_dataframe(self):
        return self._coordinate_dataframe

    def get_start_time(self):
        return self.start_time

    def get_start_time(self):
        return self.end_time
