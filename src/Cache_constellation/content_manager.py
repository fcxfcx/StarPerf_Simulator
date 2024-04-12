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
                segment_id = "v_" + str(v) + "_s_" + str(s)
                temp_segment = Segment(segment_id=segment_id, size=random.randint(1, 20))
                temp_segment_set[segment_id] = temp_segment
            video_id = "v_" + str(v)
            temp_video = Video(video_id=video_id, segment_set=temp_segment_set)
            self.content.video_set[video_id] = temp_video
        return self.content
