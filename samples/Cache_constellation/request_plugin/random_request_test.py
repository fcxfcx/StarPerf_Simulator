import src.constellation_generation.by_XML_Cache.constellation_configuration as constellation_configuration
import src.Cache_constellation.constellation_request.request_mode_plugin_manager as request_mode_manager
import h5py
import numpy as np


def random_request_test():
    dT = 1
    constellation_name = "StarLink"
    # Here wer change dT to 5730 to make constellation generation faster.
    # Because the request generation is not affected by the constellation dT here.
    constellation = constellation_configuration.constellation_configuration(dT=5730,
                                                                            constellation_name=constellation_name)
    manager = request_mode_manager.Request_mode_plugin_manager()
    manager.set_request_mode("random_request")
    manager.execute_request_policy(constellation, dT)

    file_path = "data/Cache_constellation/" + constellation.constellation_name + ".h5"
    time_slot_count = constellation.shells[-1].orbit_cycle / dT
    request_list = []
    with h5py.File(file_path, 'r') as file:
        # 指定要读取的数据集的路径
        request_group = file['request']
        for t in range(1, time_slot_count + 2, 1):
            temp_request_list = np.array(request_group["timeslot_" + str(t)]).tolist()
            request_list.append(temp_request_list)
    return request_list
