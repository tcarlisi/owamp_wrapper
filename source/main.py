"""
main.py
    Main
@author: Thomas Carlisi
"""

import sys
import time 
import signal

from owamp_api import OwampApi, InputError

def main():

    owamp = OwampApi()
    try:
        # Get info from config.ini and configure owamp
        owamp.configure()
        # Start Owamp Server
        owamp.start_server()
    except (InputError, Exception) as err:
        sys.stderr.write(str(err))
        sys.exit(1)


    # Handle program termination (Ctrl C)
    def signal_handler(signal, frame):
        print("\nprogram exiting gracefully")
        owamp.stop_server()
        owamp.stop_owping_scheduler()
        sys.exit(0)

    # TODO : GET LIST
    address_list = ["127.0.0.1", "127.0.0.1"]

    # Launch Owping (clients) Scheduler
    owamp.start_owping_scheduler(address_list)
    signal.signal(signal.SIGINT, signal_handler)

    # Infinite Loop
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
