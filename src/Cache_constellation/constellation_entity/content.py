from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Video(Base):
    __tablename__ = 'video'
    video_id = Column(Integer, primary_key=True)
    video_name = Column(String)

    def __init__(self, video_name):
        self.video_name = video_name
        self.segment_list = []


class Segment(Base):
    __tablename__ = 'segment'
    segment_id = Column(Integer, primary_key=True)
    index_in_video = Column(Integer)
    size = Column(Integer)
    video_id = Column(Integer)

    def __init__(self, index_in_video, size):
        self.index_in_video = index_in_video
        self.size = size
