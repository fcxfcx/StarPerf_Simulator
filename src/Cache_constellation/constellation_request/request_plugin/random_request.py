import h5py
import random
from src.Cache_constellation.constellation_entity import user, request
import numpy as np

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


def generate_user_request(video_count, segment_count, timeslot_count):
    # Initialization
    duration = timeslot_count  # Simulation duration
    videos = video_count  # video count
    segments = segment_count  # segment count for one video (in random plugin we assume each video has the same count)
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

    for second in range(duration):
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
                data_for_second.append((second, state['user'], state['video'], state['current_segment']))
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


def random_request(constellation, dT):
    file_path = "data/Cache_constellation/" + constellation.constellation_name + ".h5"
    with h5py.File(file_path, 'a') as file:
        # get a list of root-level group names
        root_group_names = list(file.keys())
        # if the request group is not in the root-level group of the file, create a new root-level request group.
        if 'request' not in root_group_names:
            request_group = file.create_group('request')

    # use the max orbit cycle to calculate how many time slots in this case
    sh = constellation.shells[-1]
    video_count = len(constellation.content.video_set)
    # in random plugin we assume that each video has the same segment count
    segment_count = 200
    time_slot_count = int(sh.orbit_cycle / dT)
    # generate request data for each time slot
    time_series_data = generate_user_request(video_count, segment_count, time_slot_count)

    # save the request for each time slot to h5 file
    with h5py.File(file_path, 'a') as file:
        for t in range(1, time_slot_count + 1):
            # 创建或获取时间槽的数据集
            request_group = file['request']
            request_group.create_dataset('timeslot_' + str(t), data=time_series_data[t - 1])
