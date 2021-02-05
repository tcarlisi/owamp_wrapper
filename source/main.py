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
from owping_scheduler import OwpingScheduler
import time 

import sys, signal


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
    port_range = config_info_client["port_range"]
    dhcp_value = config_info_client["dhcp_value"]
    

    # Initialize configuration
    try:
        InitConfig(user, group, dir_pid, dir_test).init_config()
    except Exception as err:
        print("Error during the configuration initialization : ", err)

    # Launch server
    server = OwampServer(dir_pid)
    server.launch_owampd()


    addr = "127.0.0.1"
    address_list = ["127.0.0.1", "127.0.0.1"]
    scheduler = OwpingScheduler(address_list, ip_version, nb_packets, 
        schedule, authentication, port_range, dhcp_value)
    scheduler.start_owping_scheduler()
    

    def signal_handler(signal, frame):
        print("\nprogram exiting gracefully")
        server.close_owampd()
        scheduler.shutdown_owping_scheduler()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
