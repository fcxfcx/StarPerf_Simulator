class content:
    def __init__(self, video_id, segment_id, size):
        self.id = "v_"+str(video_id)+"_s_"+str(segment_id)
        self.video_id = video_id
        self.segment_id = segment_id
        self.size = size
