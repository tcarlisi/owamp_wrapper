"""
config_store.py
    Store the config.ini values
@author: Thomas Carlisi
"""

import configparser

class InputError(Exception):
    """
    Exception raised for errors in the input.
    """

    def __init__(self, message):
        self.message = message

class Config_store():
    """
    Store the config.ini values
    """
    def __init__(self, config_filename):
        config_object = configparser.ConfigParser()
        config_object.read(config_filename)

        # Server information
        conf_server = config_object["CONFIG-SERVER"]
        self.user = conf_server["user"]                     # user that will execute the owamp server
        self.group = conf_server["group"]                   # group that will execute the owamp server
        self.dir_pid = conf_server["dir_pid"]               # directory that will contain the owampd pid file
        self.dir_test = conf_server["dir_test"]             # directory that will contain test temporary files

        # Client information
        conf_client = config_object["CONFIG-CLIENT"]

        self.address_list = conf_client["address_list"].split(",")  # list of address list to ping
        ipv = int(conf_client["ip_version"])
        if ipv != 0 and ipv != 4 and ipv != 6:
            raise InputError("The Ip version (in the config.ini file) must be 0, 4 or 6 (but it is : {})\n".format(ipv))
        else:
            self.ip_version = ipv                                   # IP version used by the owping

        nbp = conf_client["nb_packets"]
        if not nbp.isnumeric():
            raise InputError("The packet number (in the config.ini file) must be an integer (but it is : {})\n".format(nbp))
        else:
            self.nb_packets = int(nbp)                              # nb of packets for each test stream

        # TODO: check!
        self.pfsfile = conf_client["pfsfile"]                       # the client pfs file
        self.schedule = conf_client["schedule"]                     # the schedule of the test stream
        self.authentication = conf_client["authentication"]         # the authentication mode
        self.port_range = conf_client["port_range"]                 # port range for test stream
        self.dhcp_value = conf_client["dhcp_value"]                 # dhcp value for test stream packets
    