import random
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Float

Base = declarative_base()


class Satellite(Base):
    __tablename__ = 'satellite'
    satellite_id = Column(Integer, primary_key=True)
    longitude_str = Column(Text)
    latitude_str = Column(Text)
    altitude_str = Column(Text)
    nu = Column(Float)
    ISL_str = Column(Text)
    cache_max = Column(Integer)
    orbit_id = Column(Integer)

    def __init__(self, nu, orbit, true_satellite):
        # longitude (degree), because the satellite is constantly moving, there are many longitudes. Use the list type
        # to store all the longitudes of the satellite.
        self.longitude = []
        self.longitude_str = ""
        # latitude (degree), because the satellite is constantly moving, there are many latitudes. Use the list type
        # to store all the latitudes of the satellite.
        self.latitude = []
        self.latitude_str = ""
        # altitude (km), because the altitude is constantly moving, there are many altitudes. Use the list type
        # to store all the altitudes of the satellite.
        self.altitude = []
        self.altitude_str = ""
        # the current orbit of the satellite
        self.orbit = orbit
        # list type attribute, which stores the current satellite and which satellites have established ISL, stores
        # the ISL object
        self.ISL = []
        self.ISL_str = ""
        # True periapsis angle is a parameter that describes the position of an object in orbit. It represents the
        # angle of the object's position in orbit relative to the perigee. For different times, the value of the true
        # periapsis angle keeps changing as the object moves in its orbit.
        self.nu = nu
        # the id number of the satellite, which is the number of the satellite in the shell where it is located. If the
        # constellation has multiple shells, the id of each satellite is the number of the shell in which it is located.
        # Each shell is numbered starting from 1. The ID number is initially -1, and the user does not need to specify
        # it manually.
        self.id = -1
        # real satellite object created with sgp4 and skyfield models
        self.true_satellite = true_satellite
        # Max Cache size of this satellite
        self.cache_max = random.randrange(200, 2000, 20)
        # Cache Content, use list because every time slot has cache
        self.cache = []
        # Temp Cache size of this satellite
        self.cache_size = 0
        # User request of this satellite, use dict because not every time slot has request to this satellite
        self.requests = {}
