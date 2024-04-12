from src.Cache_constellation import content_manager


class Constellation:
    def __init__(self, constellation_name, number_of_shells, shells, dT):
        self.dT = dT
        self.constellation_name = constellation_name  # constellation name
        self.number_of_shells = number_of_shells  # the number of shells contained in the constellation
        # which shells are included in the constellation? it is a list type object, which stores shell class objects.
        self.shells = shells
        # Information about content
        self.content = content_manager.ContentManager().generate_random_content()
