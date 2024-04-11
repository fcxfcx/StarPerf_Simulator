class Content:
    def __init__(self, video_set):
        self.video_set = video_set


class Video:
    def __init__(self, video_id, segment_set):
        self.id = video_id
        self.segment_set = segment_set


class Segment:
    def __init__(self, segment_id, size):
        self.id = segment_id
        self.size = size
