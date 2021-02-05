"""
main.py
    Main
@author: Thomas Carlisi
"""

import sys
import configparser

from owamp_server import OwampServer
from owamp_client import OwampClient
from owamp_stats import OwampStats
from init_config import InitConfig
import time 


def main():

    # Get info from config.ini
    config_object = configparser.ConfigParser()
    config_object.read("../config.ini")

    config_info_server = config_object["CONFIG-SERVER"]
    user = config_info_server["user"]
    group = config_info_server["group"]
    dir_pid = config_info_server["dir_pid"]
    dir_test = config_info_server["dir_test"]
    dir_output = config_info_server["dir_output"]

    config_info_client = config_object["CONFIG-CLIENT"]
    ip_version = int(config_info_client["ip_version"])
    nb_packets = int(config_info_client["nb_packets"])
    schedule = config_info_client["schedule"]
    authentication = config_info_client["authentication"]
    dhcp_value = config_info_client["dhcp_value"]
    port_range = config_info_client["port_range"]

    # Initialize configuration
    try:
        InitConfig(user, group, dir_pid, dir_test).init_config()
    except Exception as err:
        print("Error during the configuration initialization : ", err)

    # Launch server
    server = OwampServer(dir_pid)
    server.launch_owampd()


    ip_addresses = "127.0.0.1"
    client = OwampClient(ip_addresses)
    client.owping_thread()
    client.owping_thread()
    #server.close_owampd()

if __name__ == "__main__":
    main()
