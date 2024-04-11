import src.constellation_generation.by_XML_Cache.constellation_configuration as constellation_configuration


def constellation_generation_test():
    dT = 5730
    constellation_name = "Starlink"
    # generate the constellations
    constellation = constellation_configuration.constellation_configuration(dT=dT,
                                                                            constellation_name=constellation_name)
    print('\t\t\tDetails of the constellations are as follows :')
    print('\t\t\tThe name of the constellation is : ', constellation.constellation_name)
    print('\t\t\tThe number of video in the constellation is : ', len(constellation.content.video_set))
    total_sum_segment, total_count_segment = 0, 0
    for video in constellation.content.video_set.values():
        for segment in video.segment_set.values():
            total_sum_segment += segment.size
            total_count_segment += 1
    print('\t\t\tThe average size of segment in the constellation is : ', total_sum_segment/total_count_segment)
    total_sum_cache, total_count_cache = 0, 0
    for sh in constellation.shells:
        for orbit in sh.orbits:
            for satellite in orbit.satellites:
                total_sum_cache += satellite.cache_max
                total_count_cache += 1
    print('\t\t\tThe average size of cache size in all the satellites is : ', total_sum_cache / total_count_cache)

