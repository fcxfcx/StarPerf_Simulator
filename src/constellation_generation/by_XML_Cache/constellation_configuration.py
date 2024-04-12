import json
import os
import h5py
import src.Cache_constellation.constellation_entity.shell as shell
import src.constellation_generation.by_XML_Cache.orbit_configuration as orbit_configuration
import xml.etree.ElementTree as ET
import src.Cache_constellation.constellation_entity.constellation as CONSTELLATION


def xml_to_dict(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result


def read_xml_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return {root.tag: xml_to_dict(root)}


# Parameters:
# dT : the timeslot, and the timeslot t is calculated from 0
# constellation_name : the name of the constellation to be generated, used to read the xml configuration file
def constellation_configuration(dT, constellation_name, renew):
    # the path to the constellation configuration information file .xml file
    xml_file_path = "config/XML_constellation/" + constellation_name + ".xml"
    # read constellation configuration information
    constellation_configuration_information = read_xml_file(xml_file_path)
    # convert string to int type
    number_of_shells = int(constellation_configuration_information['constellation']['number_of_shells'])
    shells = []

    for count in range(1, number_of_shells + 1, 1):
        altitude = int(constellation_configuration_information['constellation']['shell' + str(count)]['altitude'])
        orbit_cycle = int(constellation_configuration_information['constellation']['shell' + str(count)]['orbit_cycle'])
        inclination = float(
            constellation_configuration_information['constellation']['shell' + str(count)]['inclination'])
        phase_shift = int(constellation_configuration_information['constellation']['shell' + str(count)]['phase_shift'])
        number_of_orbit = int(
            constellation_configuration_information['constellation']['shell' + str(count)]['number_of_orbit'])
        number_of_satellite_per_orbit = int(
            constellation_configuration_information['constellation']['shell' + str(count)]
            ['number_of_satellite_per_orbit'])
        shell_name = "shell" + str(count)
        sh = shell.Shell(altitude=altitude, number_of_satellites=number_of_orbit * number_of_satellite_per_orbit,
                         number_of_orbits=number_of_orbit, inclination=inclination, orbit_cycle=orbit_cycle,
                         number_of_satellite_per_orbit=number_of_satellite_per_orbit, phase_shift=phase_shift,
                         shell_name=shell_name)
        # the basic properties of the sh layer have been configured. Now the track of the sh layer is generated.
        orbit_configuration.orbit_configuration(sh, dT)
        # all orbits and satellites in the sh layer have been configured. Now set the number of each satellite.
        # the number starts from 1.
        # the total number of satellites contained in the sh layer shell
        number_of_satellites_in_sh = sh.number_of_satellites
        # the total number of tracks contained in the sh layer shell
        number_of_orbits_in_sh = sh.number_of_orbits
        # in the sh layer shell, the number of satellites contained in each orbit
        number_of_satellites_per_orbit = int(number_of_satellites_in_sh / number_of_orbits_in_sh)
        # number each satellite in the sh layer, that is, modify the id attribute of the satellite object
        # traverse each orbit layer by layer, orbit_index starts from 1
        for orbit_index in range(1, number_of_orbits_in_sh + 1, 1):
            # traverse the satellites in each orbit, satellite_index starts from 1
            for satellite_index in range(1, number_of_satellites_per_orbit + 1, 1):
                satellite = sh.orbits[orbit_index - 1].satellites[satellite_index - 1]  # get satellite object
                # set the ID number of the current satellite
                satellite.id = (orbit_index - 1) * number_of_satellites_per_orbit + satellite_index
        # add the current shell layer sh to the constellation
        shells.append(sh)

    # save the shells to json
    json_shells_data = []
    for sh in shells:
        json_shells_data.append(sh.to_json())

    json_data = {
        'constellation_name': constellation_name,
        'shells': json_shells_data
    }
    # determine whether the json file exists. If it exists, delete the file and create an empty json file.
    # If it does not exist, directly create an empty json file.
    file_path = "data/Cache_constellation/" + constellation_name + "_constellation.json"
    if os.path.exists(file_path) and renew:
        # if the json file exists and needs to be renewed, delete the file
        os.remove(file_path)
    with open(file_path, 'w') as file:
        file.write(json.dumps(json_data))
    # all shells, orbits, and satellites have been initialized, and the target constellation is generated and returned.
    target_constellation = CONSTELLATION.Constellation(constellation_name=constellation_name, number_of_shells=
    number_of_shells, shells=shells, dT=dT)
    return target_constellation
