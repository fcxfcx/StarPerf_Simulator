import json
import random
from src.Cache_constellation.constellation_entity import user, request, content
import numpy as np
from math import radians, cos, sin, asin, sqrt
from tqdm import tqdm

Cities = {
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


def generate_user_request(constellation, timeslot_count):
    # Initialization
    duration = timeslot_count  # Simulation duration
    videos = len(constellation.content.video_set)  # video count
    segments = 200  # segment count for one video (in random plugin we assume each video has the same count)
    lambda_rate = 50  # Average number of new user arrival rate (per second)

    np.random.seed(42)  # want same result every time or not
    time_series_data = []

    # User arrival simulation (Poisson distribution)
    user_arrivals = np.random.poisson(lambda_rate, duration)

    # Video selection probability (power law distribution)
    video_popularity = np.random.zipf(a=2.0, size=videos)
    video_probabilities = video_popularity / np.sum(video_popularity)

    current_users = {}  # The current viewing user and their status
    user_id = 0

    for second in tqdm(range(duration), desc="Generating user request"):
        data_for_second = []
        # handle new user arrival
        for i in range(user_arrivals[second]):
            new_user = create_user()
            new_user.user_name = new_user.user_name + "_time_" + str(second) + "_no_" + str(i)
            chosen_video = np.random.choice(videos, p=video_probabilities)
            start_segment = np.random.randint(0, segments)
            watching_segments = np.random.randint(1, segments - start_segment + 1)
            current_users[user_id] = {'user': new_user, 'video': chosen_video, 'current_segment': start_segment,
                                      'remaining_segments': watching_segments}
            user_id += 1

        to_delete = []
        for user_id, state in current_users.items():
            if state['remaining_segments'] > 0:
                cur_video_id = "v_" + str(state['video'])
                cur_segment_id = "v_" + str(state['video']) + "_s_" + str(state['current_segment'])
                cur_segment = constellation.content.video_set[cur_video_id].segment_set[cur_segment_id]
                data_for_second.append(request.Request(timestamp=second, segment=cur_segment, user=state['user']))
                state['current_segment'] += 1
                state['remaining_segments'] -= 1
            if state['remaining_segments'] == 0:
                to_delete.append(user_id)  # the end of watching

        for delete_user_id in to_delete:
            del current_users[delete_user_id]
        time_series_data.append(data_for_second)

    return time_series_data


def create_user():
    # create random user
    # randomly choose a city where the user is
    city = random.choice(list(Cities.keys()))
    latitude, longitude = Cities[city]
    user_name = city
    new_user = user.User(longitude=longitude, latitude=latitude, user_name=user_name)
    return new_user


def map_requests_to_satellite(constellation, time_series_data):
    time_slot_count = len(time_series_data)
    for t in tqdm(range(time_slot_count), desc="Map Requests to Satellites"):
        temp_requests = time_series_data[t]
        for req in temp_requests:
            req_user = req.user
            target_satellite = find_nearest_satellite(constellation, req_user, t)
            # note that requests in satellite is a dict
            sat_requests = target_satellite.requests
            if t in sat_requests:
                target_satellite.requests[t].append(req)
            else:
                target_satellite.requests[t] = [req]


def find_nearest_satellite(constellation, ground_user, t):
    min_distance, target_sat = -1, None
    for sh in constellation.shells:
        for orbit in sh.orbits:
            for sat in orbit.satellites:
                temp_distance = distance_between_satellite_and_user(ground_user, sat, t)
                if temp_distance < min_distance or min_distance == -1:
                    min_distance = temp_distance
                    target_sat = sat
    return target_sat


def distance_between_satellite_and_user(ground_user, satellite, t):
    longitude1 = ground_user.longitude
    latitude1 = ground_user.latitude
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


def random_request(constellation):
    # use the min orbit cycle to calculate how many time slots in this case
    dT = constellation.dT
    min_orbit = constellation.shells[-1].orbit_cycle
    for sh in constellation.shells:
        if sh.orbit_cycle < min_orbit:
            min_orbit = sh.orbit_cycle
    video_count = len(constellation.content.video_set)
    # in random plugin we assume that each video has the same segment count
    segment_count = 200
    time_slot_count = int(min_orbit / dT)
    # generate request data for each time slot
    time_series_data = generate_user_request(constellation, time_slot_count)
    map_requests_to_satellite(constellation, time_series_data)

    # file_path = "data/Cache_constellation/" + constellation.constellation_name + "_requests.json"
    # json_data = {"Requests": time_series_data}
    # # save the request for each time slot to h5 file
    # with open(file_path, 'w') as file:
    #     file.write(json.dumps(json_data))
