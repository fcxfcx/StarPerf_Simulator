import random
from src.Cache_constellation.constellation_entity.content import *


class ContentManager:
    def __init__(self):
        self.video_list = []

    # generate some content with random size
    def generate_random_content(self):
        for v in range(0, 20):
            temp_segment_list = []
            for s in range(0, 200):
                temp_segment = Segment(size=random.randint(5, 20), index_in_video=s)
                temp_segment_list.append(temp_segment)
            temp_video = Video(video_name="v_"+str(v))
            temp_video.segment_list = temp_segment_list
            self.video_list.append(temp_video)
        return self.video_list
