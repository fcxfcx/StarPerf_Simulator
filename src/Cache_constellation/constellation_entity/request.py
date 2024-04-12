class Request:
    def __init__(self, timestamp, segment, user):
        self.timestamp = timestamp
        self.segment = segment
        self.user = user

    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'segment': self.segment.to_json(),
            'user': self.user.to_json()
        }
