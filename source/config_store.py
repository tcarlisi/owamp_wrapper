"""
config_store.py
    Store the config.ini values
@author: Thomas Carlisi
"""

import re 
import fnmatch

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
        self.owamp_executable = conf_server["owamp_executable"]     # owamp executable
        self.user = conf_server["user"]                             # user that will execute the owamp server
        self.group = conf_server["group"]                           # group that will execute the owamp server
        self.dir_pid = conf_server["dir_pid"]                       # directory that will contain the owampd pid file
        self.dir_test = conf_server["dir_test"]                     # directory that will contain test temporary files
        self.server_config_dir = conf_server["server_config_dir"]   # server configuration directory

        # Client information
        conf_client = config_object["CONFIG-CLIENT"]
        self.owping_executable = conf_client["owping_executable"]   # owping executable
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

        pfs = conf_client["pfsfile"] 
        if not fnmatch.fnmatch(pfs, '*.pfs'):
            raise InputError("The pfs file must be a valid filename with extension '.pfs' (but it is : {})\n".format(pfs))
        self.pfsfile = pfs                                          # the client pfs file

        # Checked by owping program
        self.schedule = conf_client["schedule"]                     # the schedule of the test stream
        
        pr = conf_client["port_range"]
        if not re.fullmatch("^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$", pr):
            raise InputError("The port format is not respected : 0-65535 (but it is : {})\n".format(pr))
        else:
            self.port_range = pr                                    # port range for test stream
        
        # Checked by owping program
        self.dhcp_value = conf_client["dhcp_value"]                 # dhcp value for test stream packets
    