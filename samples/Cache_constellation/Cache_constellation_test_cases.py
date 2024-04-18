from src.Cache_constellation.constellation_cache import cache_mode_plugin_manager
from src.Cache_constellation.manager.city_manager import CityManager
from src.Cache_constellation.manager.content_manager import ContentManager
from src.Cache_constellation.manager.database_manager import DatabaseManager
from src.Cache_constellation.manager.request_manager import RequestManager
from src.constellation_generation.by_XML_Cache import constellation_configuration
import matplotlib.pyplot as plt


def Cache_constellation_test_cases():
    database_manager = DatabaseManager()
    print("Test 1 : constellation generation test")
    # constellation generation test
    dT = 5717
    constellation_name = "Test_Constellation"
    # generate the constellations
    constellation = (constellation_configuration.constellation_configuration
                     (dT=dT, constellation_name=constellation_name))
    database_manager.add_constellation(constellation)

    print("Test 2 : content generation test")
    content_manager = ContentManager()
    video_list = content_manager.generate_random_content()
    database_manager.add_content(video_list)

    print("Test 3 : city generation test")
    city_manager = CityManager()
    city_list = city_manager.get_city_list()
    database_manager.add_city(city_list)
    mapping = city_manager.mapping_city(constellation)
    database_manager.add_city_service(mapping)

    print("Test 4 : random request generation test")
    # random request generation test
    request_manager = RequestManager(constellation, database_manager)
    request_list = request_manager.generate_random_request(video_list, city_list)
    database_manager.add_request(request_list)

    print("Test 5 : LFU Cache test")
    cache_manager = cache_mode_plugin_manager.Cache_mode_plugin_manager(database_manager)
    cache_manager.set_cache_mode("LFU")
    cache_manager.execute_cache_policy(constellation)
    database_manager.add_cache_segment(constellation, "LFU")

    # print("Drawing cache hit ratio figure...")
    # hit_ratio = []
    # for t, temp_req_list in enumerate(constellation.requests):
    #     if t == 0:
    #         # time 0 is not valid
    #         continue
    #     else:
    #         hit_count = 0
    #         total_count = len(temp_req_list)
    #         for req in temp_req_list:
    #             target_sat = req.target
    #             if req.segment.id in target_sat.cache[t - 1]:
    #                 hit_count += 1
    #         hit_ratio.append(hit_count / total_count * 100)
    # plt.plot(hit_ratio)
    # plt.title("LFU Cache hit")
    # plt.xlabel("Timestamp")
    # plt.ylabel("Hit Ratio")
    # plt.show()


if __name__ == "__main__":
    Cache_constellation_test_cases()
