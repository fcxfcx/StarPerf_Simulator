class ground_station:
    def __init__(self , longitude, latitude , description = None , frequency=None , antenna_count = None ,
                 uplink_GHz = None , downlink_GHz = None):
        self.longitude = longitude # the longitude of GS
        self.latitude = latitude # the latitude of GS
        self.description = description  # the description of GS's position
        self.frequency = frequency # the frequency of GS, such as Ka,E and so on
        self.antenna_count = antenna_count # the number of antenna of GS
        self.uplink_GHz = uplink_GHz # the uplink GHz of GS
        self.downlink_GHz = downlink_GHz # the downlink GHz of GS