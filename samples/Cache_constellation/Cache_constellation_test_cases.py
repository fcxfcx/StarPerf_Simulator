from src.Cache_constellation.constellation_cache import cache_mode_plugin_manager
from src.constellation_generation.by_XML_Cache import constellation_configuration
from src.Cache_constellation.constellation_request import request_mode_plugin_manager


def Cache_constellation_test_cases():
    print("\t\t\033[31mTest(1/3) : constellation generation\033[0m")
    # constellation generation test
    dT = 500
    constellation_name = "Starlink"
    # generate the constellations
    constellation = (constellation_configuration.
                     constellation_configuration(dT=dT, constellation_name=constellation_name, renew=True))
    print('\t\t\tDetails of the constellations are as follows :')
    print('\t\t\tThe name of the constellation is : ', constellation.constellation_name)
    print('\t\t\tThe number of video in the constellation is : ', len(constellation.content.video_set))
    total_sum_segment, total_count_segment = 0, 0
    for video in constellation.content.video_set.values():
        for segment in video.segment_set.values():
            total_sum_segment += segment.size
            total_count_segment += 1
    print('\t\t\tThe average size of segment in the constellation is : ', total_sum_segment / total_count_segment)
    total_sum_cache, total_count_cache = 0, 0
    for sh in constellation.shells:
        for orbit in sh.orbits:
            for satellite in orbit.satellites:
                total_sum_cache += satellite.cache_max
                total_count_cache += 1
    print('\t\t\tThe average size of cache size in all the satellites is : ', total_sum_cache / total_count_cache)

    print("\t\t\033[31mTest(2/3) : random request generation test\033[0m")
    # random request generation test
    constellation_name = "StarLink"
    manager = request_mode_plugin_manager.Request_mode_plugin_manager()
    manager.set_request_mode("random_request")
    manager.execute_request_policy(constellation)

    print("\t\t\033[31mTest(3/3) : LFU Cache test\033[0m")
    manager = cache_mode_plugin_manager.Cache_mode_plugin_manager()
    manager.set_cache_mode("LFU")
    manager.execute_cache_policy(constellation)



if __name__ == "__main__":
    Cache_constellation_test_cases()
