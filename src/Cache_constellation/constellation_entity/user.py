from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    city_id = Column(Integer)

    def __init__(self, user_name, city_id):
        self.user_name = user_name  # the name of user
        self.city_id = city_id
        self.request_list = []  # the request list during one loop
