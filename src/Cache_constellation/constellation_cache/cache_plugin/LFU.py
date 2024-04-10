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