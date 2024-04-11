import random
from src.Cache_constellation.constellation_entity.content import *


class ContentManager:
    def __init__(self):
        self.content = Content(dict())

    # generate some content with random size
    def generate_random_content(self):
        for v in range(0, 20):
            temp_segment_set = dict()
            for s in range(0, 200):
                temp_segment = Segment(segment_id=s, size=random.randint(1, 20))
                temp_segment_set["s_" + str(s)] = temp_segment
            temp_video = Video(video_id=v, segment_set=temp_segment_set)
            self.content.video_set["v_" + str(v)] = temp_video
        return self.content
