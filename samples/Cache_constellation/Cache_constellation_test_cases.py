import samples.Cache_constellation.request_plugin.random_request_test
from samples.Cache_constellation.constellation_generation import constellation_generation_test
from samples.Cache_constellation.request_plugin import random_request_test


def Cache_constellation_test_cases():
    print("\t\t\033[31mTest(01/16) : constellation generation\033[0m")
    # constellation generation test
    constellation_generation_test.constellation_generation_test()

    print("\t\t\033[31mTest(02/16) : random request generation test\033[0m")
    # random request generation test
    request_list = random_request_test.random_request_test()
    print(request_list)


if __name__ == "__main__":
    Cache_constellation_test_cases()
