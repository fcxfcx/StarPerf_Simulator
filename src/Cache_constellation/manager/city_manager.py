import random
from src.Cache_constellation.constellation_entity.city import City
from math import radians, cos, sin, asin, sqrt
import numpy as np


def find_nearest_satellite(constellation, longitude, latitude, t) -> (int, int, int):
    min_distance, target_shell, target_orbit, target_sat = -1, -1, -1, -1
    for sh in constellation.shells:
        for orbit in sh.orbits:
            for sat in orbit.satellites:
                temp_distance = distance_between_satellite_and_user(longitude, latitude, sat, t)
                if temp_distance < min_distance or min_distance == -1:
                    min_distance = temp_distance
                    target_sat = sat.satellite_id
    return target_sat


def distance_between_satellite_and_user(longitude, latitude, satellite, t):
    longitude1 = longitude
    latitude1 = latitude
    longitude2 = satellite.longitude[t]
    latitude2 = satellite.latitude[t]
    # convert latitude and longitude to radians
    longitude1, latitude1, longitude2, latitude2 = map(radians, [float(longitude1), float(latitude1), float(longitude2),
                                                                 float(latitude2)])
    dlon = longitude2 - longitude1
    dlat = latitude2 - latitude1
    a = sin(dlat / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371.0 * 1000  # the average radius of the earth is 6371km
    # convert the result to kilometers with three decimal places.
    distance = np.round(distance / 1000, 3)
    return distance


class CityManager:
    def __init__(self):
        self.city_dict = {
            "New York": (40.7128, -74.0060),
            "London": (51.5074, -0.1278),
            "Tokyo": (35.6895, 139.6917),
            "Paris": (48.8566, 2.3522),
            "Sydney": (-33.8651, 151.2099),
            "Berlin": (52.5200, 13.4050),
            "Toronto": (43.65107, -79.347015),
            "Rome": (41.9028, 12.4964),
            "Cairo": (30.0444, 31.2357),
            "Moscow": (55.751244, 37.618423),
            "San Francisco": (37.7749, -122.4194),
            "Beijing": (39.9042, 116.4074),
            "Dubai": (25.2048, 55.2708),
            "Mumbai": (19.0760, 72.8777),
            "Rio de Janeiro": (-22.9068, -43.1729),
            "Singapore": (1.3521, 103.8198),
            "Cape Town": (-33.9249, 18.4241),
            "Buenos Aires": (-34.6037, -58.3816),
            "Chicago": (41.8781, -87.6298)
        }
        self.city_list = []

    def get_random_city(self):
        city_name = random.choice(list(self.city_dict.keys()))
        latitude, longitude = self.city_dict[city_name]
        return city_name, latitude, longitude

    def get_city_list(self):
        if len(self.city_list) == 0:
            for city_name, (latitude, longitude) in self.city_dict.items():
                temp_city = City(city_name, latitude, longitude)
                self.city_list.append(temp_city)
        return self.city_list

    def mapping_city(self, constellation):
        city_list = self.get_city_list()
        mapping = {}
        time_slot_count = constellation.get_time_slot_count()
        for city in city_list:
            time_series_data = []
            latitude, longitude = city.latitude, city.longitude
            for t in range(0, time_slot_count):
                sat_index = find_nearest_satellite(constellation, latitude, longitude, t)
                time_series_data.append(sat_index)
            mapping[city.city_id] = time_series_data
        return mapping
