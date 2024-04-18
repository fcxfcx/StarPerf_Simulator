from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, city_name, latitude, longitude):
        self.city_name = city_name
        self.latitude = latitude
        self.longitude = longitude
