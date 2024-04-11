class User:
    def __init__(self, longitude, latitude, user_name=None):
        self.user_name = user_name  # the name of user
        self.longitude = longitude  # the longitude of user
        self.latitude = latitude  # the latitude of user
        self.request_list = []    # the request list during one loop
