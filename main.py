"""
main.py
    Main
@author: Thomas Carlisi
"""

import sys
import configparser

from owamp_server import OwampServer
from owamp_client import OwampClient
from init_config import InitConfig
import time 


def main():

    # Get info from config.ini
    config_object = configparser.ConfigParser()
    config_object.read("config.ini")

    config_info = config_object["CONFIG-OWAMP"]
    user = config_info["user"]
    group = config_info["group"]
    dir_pid = config_info["dir_pid"]
    dir_test = config_info["dir_test"]
    dir_output = config_info["dir_output"]

    # Initialize configuration
    try:
        InitConfig(user, group, dir_pid, dir_test).init_config()
    except Exception as err:
        print("Error during the configuration initialization : ", err)



    # Launch Client or Server
    if int(sys.argv[1]) == 0:
        print("---------------Mode 0---------------")
        server = OwampServer(dir_pid)
        server.launch_owampd()
        ip_addresses = ["127.0.0.1"]
        client = OwampClient(ip_addresses, dir_output)
        client.owping()
        client.owping()
        server.close_owampd()


    elif int(sys.argv[1]) == 1:
        print("---------------Mode 1---------------")


    else:
        print("arg1 must be 0 (Server) or 1 (Client)")

if __name__ == "__main__":
    main()
