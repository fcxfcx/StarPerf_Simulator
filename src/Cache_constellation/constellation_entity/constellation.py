from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Constellation(Base):
    __tablename__ = 'constellation'
    constellation_id = Column(Integer, primary_key=True)
    constellation_name = Column(String(64), unique=True)
    number_of_shells = Column(Integer)
    dT = Column(Integer)

    def __init__(self, constellation_name, number_of_shells, shells, dT):
        self.dT = dT
        self.constellation_name = constellation_name  # constellation name
        self.number_of_shells = number_of_shells  # the number of shells contained in the constellation
        # which shells are included in the constellation? it is a list type object, which stores shell class objects.
        self.shells = shells
        self.video_list = []
        self.time_slot_count = -1

    def get_time_slot_count(self):
        if self.time_slot_count == -1:
            min_orbit = self.shells[-1].orbit_cycle
            for sh in self.shells:
                if sh.orbit_cycle < min_orbit:
                    min_orbit = sh.orbit_cycle
            self.time_slot_count = int(min_orbit / self.dT)
        return self.time_slot_count
