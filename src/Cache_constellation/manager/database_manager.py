from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from src.Cache_constellation.constellation_entity.cache_segment import CacheSegment
from src.Cache_constellation.constellation_entity.city import City
from src.Cache_constellation.constellation_entity.request import Request
from src.Cache_constellation.constellation_entity.city_service import CityService
from src.Cache_constellation.constellation_entity.content import Segment


class DatabaseManager:
    def __init__(self):
        engine = create_engine("mysql+pymysql://root:123456@localhost:3306/constellation_sim?charset=utf8")
        Session = sessionmaker(bind=engine)
        self.session = Session()

    # save constellation to database
    # including constellation, shell, orbit, satellite
    def add_constellation(self, constellation):
        self.session.add(constellation)
        self.session.commit()
        constellation_id = constellation.constellation_id
        print("Starting Adding Constellation")
        for sh in tqdm(constellation.shells, desc="Adding Shells"):
            sh.constellation_id = constellation_id
            self.session.add(sh)
            self.session.flush()
            shell_id = sh.shell_id
            for orbit in sh.orbits:
                orbit.shell_id = shell_id
                self.session.add(orbit)
                self.session.flush()
                orbit_id = orbit.orbit_id
                for sat in orbit.satellites:
                    sat.orbit_id = orbit_id
                    # transform list to string to store
                    sat.longitude_str = ','.join(str(x) for x in sat.longitude)
                    sat.latitude_str = ','.join(str(x) for x in sat.latitude)
                    sat.altitude_str = ','.join(str(x) for x in sat.altitude)
                    sat.ISL_str = ','.join(str(x) for x in sat.ISL)
                    self.session.add(sat)
        print("Start Commit Constellation")
        self.session.commit()
        print("End Commit Constellation")

    # save content to database, including video and segment
    def add_content(self, video_list):
        print("Start Adding Video content")
        for v in tqdm(video_list, desc="Adding Videos"):
            self.session.add(v)
            self.session.flush()
            video_id = v.video_id
            for segment in v.segment_list:
                segment.video_id = video_id
                self.session.add(segment)
        print("Start Commit Video content")
        self.session.commit()
        print("End Commit Video content")

    # get segment id by video id and its index in the video
    def get_segment_id(self, video_id, index_in_video):
        result = self.session.query(Segment.segment_id).filter(
            Segment.video_id == video_id,
            Segment.index_in_video == index_in_video
        ).one()
        return result[0]

    # save cities to database
    def add_city(self, city_list):
        for city in city_list:
            self.session.add(city)
        self.session.commit()

    def get_city_index_list(self):
        result = self.session.query(City).all()
        city_index_list = [row.city_id for row in result]
        return city_index_list

    def add_city_service(self, city_mapping):
        for city_index, time_series_data in city_mapping.items():
            for t, satellite_index in enumerate(time_series_data):
                temp_city_service = CityService(city_index, satellite_index, t)
                self.session.add(temp_city_service)
        self.session.commit()

    def get_city_service(self, city_index, timeslot):
        result = self.session.query(CityService.satellite_id).filter(
            CityService.city_id == city_index,
            CityService.timeslot == timeslot
        ).first()
        return result[0]

    def add_request(self, request_list):
        for req in request_list:
            self.session.add(req)
        self.session.commit()

    def get_request_by_satellite(self, satellite_id, timeslot):
        result = self.session.query(Request).filter(
            Request.satellite_id == satellite_id,
            Request.timeslot == timeslot
        ).all()
        return result

    def get_segment_size(self, segment_id):
        result = self.session.query(Segment.size).filter(Segment.segment_id == segment_id).first()
        return result[0]

    # save cache by cache list of certain satellite
    def add_cache_segment(self, constellation, cache_strategy):
        for sh in constellation.shells:
            for orbit in sh.orbits:
                for sat in orbit.satellites:
                    sat_id = sat.satellite_id
                    for t, cache_t in enumerate(sat.cache):
                        cache_content_str = ','.join(str(x) for x in cache_t)
                        new_cache_segment = CacheSegment(sat_id, t, cache_content_str, cache_strategy)
                        self.session.add(new_cache_segment)
        self.session.commit()
