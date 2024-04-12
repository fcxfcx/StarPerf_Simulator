import json
from tqdm import tqdm


def LFU(constellation):
    dT = constellation.dT
    # generate cache data for each shell and each satellite
    shell_tqdm = tqdm(constellation.shells)
    for shell in shell_tqdm:
        shell_tqdm.set_description("Simulating Shell " + str(shell.shell_name) + ":")

        sat_cache_json_data = []
        time_slot_count = shell.orbit_cycle / dT
        for orbit in shell.orbits:
            for sat in orbit.satellites:
                temp_cache = LFUCache(sat.cache_max)
                cache_list = []
                request_list = sat.requests
                # make sure the number of time slot is the same between cache module and request module
                if len(request_list) != time_slot_count:
                    print("Error: time slot count is different between cache module and request module for shell"
                          + shell.shell_name + " and satellite " + sat.id)
                    return
                sat_tqdm = tqdm(range(0, time_slot_count + 1))
                for t in sat_tqdm:
                    sat_tqdm.set_description("Simulating Satellite " + str(sat.id) + ":")
                    for request in request_list[t]:
                        temp_segment = request.segment
                        temp_cache.put(temp_segment.id, temp_segment)
                    cache_list.append(temp_cache.get_cache_contents())
                sat.cache = cache_list


class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.min_freq = 0  # Track the minimum frequency
        self.key_to_val = {}  # Key to Value mapping (Value here is the segment object)
        self.key_to_freq = {}  # Key to Frequency mapping
        self.freq_to_keys = {}  # Frequency to Keys mapping
        self.current_size = 0  # Track current stored size

    def get(self, key):
        if key not in self.key_to_val:
            return -1
        # Increase the frequency of the key
        self.increase_freq(key)
        return self.key_to_val[key]

    def put(self, key, segment):
        if self.capacity <= 0:
            return

        size = segment.size  # Assuming segment object has a 'size' attribute
        if key in self.key_to_val:
            self.current_size -= self.key_to_val[key].size  # Remove old size
            self.current_size += size  # Add new size
            self.key_to_val[key] = segment
            self.increase_freq(key)
            return

        while self.current_size + size > self.capacity and self.key_to_val:
            self.remove_min_freq_key()

        if self.current_size + size <= self.capacity:
            self.key_to_val[key] = segment
            self.key_to_freq[key] = 1
            self.freq_to_keys.setdefault(1, set()).add(key)
            self.min_freq = 1  # Reset min_freq to 1 for the new key
            self.current_size += size

    def get_cache_contents(self) -> list:
        return list(self.key_to_val.keys())

    def increase_freq(self, key):
        freq = self.key_to_freq[key]
        # Update key's frequency
        self.key_to_freq[key] = freq + 1
        # Remove the key from the old freq set
        self.freq_to_keys[freq].remove(key)
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if freq == self.min_freq:
                self.min_freq += 1
        # Add the key to the new freq set
        self.freq_to_keys.setdefault(freq + 1, set()).add(key)

    def remove_min_freq_key(self):
        # Find the least frequently used keys
        keys = self.freq_to_keys[self.min_freq]
        # Remove the first least frequently used key
        key = keys.pop()
        if not keys:
            del self.freq_to_keys[self.min_freq]
        # Remove the least frequently used key from key_to_val and key_to_freq
        removed_segment = self.key_to_val.pop(key)
        del self.key_to_freq[key]
        self.current_size -= removed_segment.size  # Update current size after removal
