from src.Cache_constellation.constellation_entity import request
import numpy as np
from tqdm import tqdm


class RequestManager:
    def __init__(self, constellation, database_manager):
        self.constellation = constellation
        self.database_manager = database_manager

    def generate_random_request(self, video_list, city_list):
        # Initialization
        duration = self.constellation.get_time_slot_count()  # Simulation duration
        city_count = len(city_list)
        video_count = len(video_list)  # video count
        segment_count = len(video_list[0].segment_list)  # segment count for one video
        lambda_rate = 50  # Average number of new user arrival rate (per second)

        np.random.seed(42)  # want same result every time or not
        request_list = []

        # User arrival simulation (Poisson distribution)
        user_arrivals = np.random.poisson(lambda_rate, duration)

        # Video selection probability (power law distribution)
        video_popularity = np.random.zipf(a=2.0, size=video_count)
        video_probabilities = video_popularity / np.sum(video_popularity)

        current_users = {}  # The current viewing user and their status
        user_id = 0

        for second in tqdm(range(duration), desc="Generating user request"):
            data_for_second = []
            # handle new user arrival
            for i in range(user_arrivals[second]):
                chosen_city = np.random.choice(city_list)
                chosen_city_index = chosen_city.city_id
                chosen_video = np.random.choice(video_list, p=video_probabilities)
                chosen_video_index = chosen_video.video_id
                start_segment_index = np.random.randint(0, segment_count)
                watching_segments = np.random.randint(1, segment_count - start_segment_index + 1)
                current_users[user_id] = {'city': chosen_city_index,
                                          'video': chosen_video_index,
                                          'current_segment': start_segment_index,
                                          'remaining_segments': watching_segments}
                user_id += 1

            to_delete = []
            for user_id, state in current_users.items():
                if state['remaining_segments'] > 0:
                    cur_video_index, cur_segment_index = state['video'], state['current_segment']
                    cur_segment_id = self.database_manager.get_segment_id(cur_video_index, cur_segment_index)
                    cur_city_id = state['city']
                    request_list.append(
                        request.Request(timeslot=second, segment_id=cur_segment_id, city_id=cur_city_id))
                    state['current_segment'] += 1
                    state['remaining_segments'] -= 1
                if state['remaining_segments'] == 0:
                    to_delete.append(user_id)  # the end of watching

            for delete_user_id in to_delete:
                del current_users[delete_user_id]

        for req in tqdm(request_list, desc="Map Requests to Satellites"):
            req_city = req.city_id
            sat_id = self.database_manager.get_city_service(city_index=req_city, timeslot=req.timeslot)
            req.satellite_id = sat_id

        return request_list



