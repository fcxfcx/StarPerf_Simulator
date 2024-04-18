from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

Base = declarative_base()


class Request(Base):
    __tablename__ = 'request'
    request_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    satellite_id = Column(Integer)
    segment_id = Column(Integer)
    timeslot = Column(Integer)

    def __init__(self, timeslot, segment_id, city_id):
        self.timeslot = timeslot
        self.segment_id = segment_id
        self.city_id = city_id
