import h5py


def LFU(constellation, dT):
    file_path = "data/Cache_constellation/" + constellation.constellation_name + ".h5"
    with h5py.File(file_path, 'a') as file:
        # get a list of root-level group names
        root_group_names = list(file.keys())
        # if the cache group is not in the root-level group of the file, create a new root-level cache group.
        if 'cache' not in root_group_names:
            cache_group = file.create_group('cache')
            # create multiple shell subgroups within the delay group. For example, the shell1 subgroup represents the
            # first-level shell, the shell2 subgroup represents the second-level shell, etc.
            for count in range(1, constellation.number_of_shells + 1, 1):
                cache_group.create_group('shell' + str(count))

    for sh_index, sh in enumerate(constellation.shells):
        # the total number of satellites contained in the sh layer shell
        number_of_satellites_in_sh = sh.number_of_satellites
        # the total number of tracks contained in the sh layer shell
        number_of_orbits_in_sh = sh.number_of_orbits
        # in the sh layer shell, the number of satellites contained in each orbit
        number_of_satellites_per_orbit = (int)(number_of_satellites_in_sh / number_of_orbits_in_sh)

        # update cache for each satellite
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):
            # traverse the satellites in each orbit, satellite_index starts from 1
            for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):
                # get the current satellite object
                cur_satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]
                # get the id of the current satellite
                cur_satellite_id = cur_satellite.id