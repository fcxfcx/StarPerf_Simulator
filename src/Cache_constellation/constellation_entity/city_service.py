from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class CityService(Base):
    __tablename__ = 'city_service'
    city_service_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    satellite_id = Column(Integer)
    timeslot = Column(Integer)

    def __init__(self, city_id, satellite_id, timeslot):
        self.city_id = city_id
        self.satellite_id = satellite_id
        self.timeslot = timeslot
