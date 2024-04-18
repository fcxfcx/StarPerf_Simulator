from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String

Base = declarative_base()


class CacheSegment(Base):
    __tablename__ = 'cache_segment'
    cache_segment_id = Column(Integer, primary_key=True)
    satellite_id = Column(Integer)
    timeslot = Column(Integer)
    cache_content_str = Column(Text)
    cache_strategy = Column(String)

    def __init__(self, satellite_id, timeslot, cache_content_str, cache_strategy):
        self.satellite_id = satellite_id
        self.timeslot = timeslot
        self.cache_content_str = cache_content_str
        self.cache_strategy = cache_strategy
