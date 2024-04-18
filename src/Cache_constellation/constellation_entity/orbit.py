import math
from poliastro.bodies import Earth
from poliastro.twobody import Orbit as TwobodyOrbit
from astropy import units as u
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class Orbit(Base):
    __tablename__ = 'orbit'
    orbit_id = Column(Integer, primary_key=True)
    orbit_name = Column(String)
    orbit_cycle = Column(Float)
    shell_id = Column(Integer)

    def __init__(self, a, ecc, inc, raan, argp, orbit_name):
        self.orbit_name = orbit_name
        self.a = a * u.km  # the semi-major axis of the orbit in kilometers km
        self.ecc = ecc * u.one  # orbital eccentricity
        self.inc = inc * u.deg  # the inclination of the orbit in degrees
        self.raan = raan * u.deg  # orbit ascending node right ascension
        self.argp = argp * u.deg  # perigee argument in degrees
        # # calculate orbital period (unit: s)
        self.orbit_cycle = 2 * math.pi * math.sqrt((a * 1000) ** 3 / (6.67430e-11 * 5.972e24))
        # actual satellite orbit
        self.satellite_orbit = TwobodyOrbit.from_classical(
            Earth,
            a=self.a,
            ecc=self.ecc,
            inc=self.inc,
            raan=self.raan,
            argp=self.argp,
            # True periapsis angle is used to describe the satellite. Here is the generated orbit. This parameter
            # has no effect and only takes up space.
            nu=0 * u.deg
        )
        # a list type field is used to store satellites in the orbit and stores satellite objects.
        self.satellites = []
