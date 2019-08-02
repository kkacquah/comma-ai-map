import json
import datetime
from os import listdir
from Trip import Trip
from os.path import isfile, join
import pandas as pd
from colour import Color

ISO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
TRIPS_FOLDER_PATH = './trips'
TRIPS_FOLDER_PATH_FORMAT = './trips/%s'
SPEED_TO_COLOR_DECIMAL_PLACES = 1
GRADIENT_BEGIN = "yellow"
GRADIENT_END = "red"

class AggregateTrips(object):

    def __init__(self, trip_folder):
        # Trip is a list of dictionaries with the following format
        # {"lat": 37.25585893874121,
        # "speed": 26.30250495735354,
        # "lng": -122.41407280418797,
        # "dist": 7.1663417633771935,
        # "index": 486}

        # start_time and end_time are the beginning and the end of the trip
        trip_list = self._read_trips_from_folder(trip_folder)
        self._aggregate_coordinate_dataframe = self._get_aggregate_coordinates_dataframe_from_trip_list(trip_list)
        self._trip_speed_max, self._trip_speed_min = self._get_trip_max_and_min()
        #for comparing other speed against for coloring
        self._trunc_min_speed = round(self._trip_speed_min,SPEED_TO_COLOR_DECIMAL_PLACES)
        self._aggregate_trip_gradient = self._get_speed_gradient()
        self._aggregate_trip_data = self._get_aggregate_coordinates_info()
        print(self._aggregate_trip_data)

    def _read_trips_from_folder(self, trip_folder):
        trip_filenames = [file for file  in listdir(trip_folder) if isfile(join(trip_folder, file))]
        trip_list = []
        for filename in trip_filenames[:200]:
            trip_filepath = TRIPS_FOLDER_PATH_FORMAT % filename
            with open(trip_filepath) as file: # Use file to refer to the file object
                trip_list.append(Trip(file))
        return trip_list

    def _get_trip_max_and_min(self):
        trip_speed_max = self._aggregate_coordinate_dataframe['speed'].max()
        trip_speed_min = self._aggregate_coordinate_dataframe['speed'].min()
        return trip_speed_max, trip_speed_min

    def _get_aggregate_coordinates_info(self):
        aggregate_trip_data = self._split_into_latitute_longitude_buckets()
        return aggregate_trip_data

    def _get_speed_gradient(self):
        trunc_max_speed = round(self._trip_speed_max,SPEED_TO_COLOR_DECIMAL_PLACES)
        number_of_colors = int((trunc_max_speed - self._trunc_min_speed) * 10)
        yellow = Color(GRADIENT_BEGIN)
        return list(yellow.range_to(Color(GRADIENT_END),number_of_colors+1))

    def _get_color_hex_from_speed(self, speed):
        trunc_speed = round(speed,SPEED_TO_COLOR_DECIMAL_PLACES)
        color_index =int((trunc_speed - self._trunc_min_speed) * 10)
        return self._aggregate_trip_gradient[color_index].hex

    def _split_into_latitute_longitude_buckets(self):
        #a bucket represents a longitude and latitude of a
        #with all speeds travelled at that coordinate, and the average of
        #all speeds travelled at that coordinate
        buckets = []
        prev_lng = 0
        prev_lat = 0
        prev_prev_lng = 0
        prev_prev_lat = 0
        bucket = None
        for _, row in self._aggregate_coordinate_dataframe.iterrows():
            #if this lat and lng has not been seen before
            if prev_lng != row["lng"] or prev_lat != row["lat"] or prev_prev_lng != row["prev_lng"] or prev_prev_lat != row["prev_lat"]:
                #add old bucket to list and initialize a new one
                if(bucket):
                    avg_speed = sum(bucket["speeds"])/len(bucket["speeds"])
                    bucket["avg_speed"] = avg_speed
                    bucket["color"] = self._get_color_hex_from_speed(avg_speed)
                    bucket["speeds"] = []
                    #reset prev lat and lng to bucket being added
                    #append bucket to bucket list
                    buckets.append(bucket)
                bucket = dict()
                #create new bucket
                #set bucket values
                bucket["lng"] = row["lng"]
                bucket["lat"] = row["lat"]
                bucket["prev_lng"] =  row["prev_lng"]
                bucket["prev_lat"] = row["prev_lat"]
                prev_lng = row["lng"]
                prev_lat = row["lat"]
                prev_prev_lng = row["prev_lng"]
                prev_prev_lat =  row["prev_lat"]
                bucket["speeds"] = [row["speed"]]
            #if it has been seen before
            else:
                bucket["speeds"].append(row["speed"])
        #add last created bucket to the bucket list
        buckets.append(bucket)

        return buckets

        for filename in trip_filenames:
            trip_filepath = TRIPS_FOLDER_PATH_FORMAT % filename
            with open(trip_filepath) as file: # Use file to refer to the file object
                trip_list.append(Trip(file))
        return trip_list

    def _sort_dataframe_by_lng_and_lat(self, aggregate_coordinate_dataframe):
        aggregate_coordinate_dataframe = aggregate_coordinate_dataframe.sort_values(by=['lng','lng','prev_lng','prev_lat'])
        return aggregate_coordinate_dataframe

    def _get_aggregate_coordinates_dataframe_from_trip_list(self, trip_list):
        aggregate_coordinate_dataframe = pd.DataFrame()
        for trip in trip_list:
            aggregate_coordinate_dataframe = aggregate_coordinate_dataframe.append(trip.get_coordinate_dataframe(), ignore_index = True)
            aggregate_coordinate_dataframe = self._sort_dataframe_by_lng_and_lat(aggregate_coordinate_dataframe)
        return aggregate_coordinate_dataframe

    def get_trip_list(self):
        return self._trip_list

    def get_aggregate_coordinate_dataframe(self):
        return self._aggregate_coordinate_dataframe

aggregatedTrips = AggregateTrips(TRIPS_FOLDER_PATH)
