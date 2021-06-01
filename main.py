"""
main.py
    Main
@author: Thomas Carlisi
"""

import sys
import time 
import signal

from source.owamp_api import OwampApi, InputError, OwampStats

def main():

    owamp = OwampApi()
    try:
        # Get info from config.ini and configure owamp
        print("Dev: OWAMP Config initialization...")
        owamp.configure("./config.ini")
        # Start Owamp Server
        owamp.start_server()
        print("Dev: OWAMP Server started...")

    except (InputError, KeyError, Exception) as err:
        sys.stderr.write(str(err))
        sys.exit(1)


    # Handle program termination (Ctrl C)
    def signal_handler(signal, frame):
        print("\nprogram exiting gracefully")
        owamp.stop_server()
        owamp.stop_owping_scheduler()
        sys.exit(0)

    def scheduler_callback(owamp_stats:OwampStats):
        print("Job worked")
        owamp_stats._debug_print_stats()

    def scheduler_callback_ping_failed(owamp_stats:OwampStats, stderr):
        print("Ping failed")    
        message = "Owping for address {addr} did not work".format(addr=owamp_stats.address)
        print(message)
        print("owping program error:\n", stderr)

    def scheduler_callback_fail():
        print("Job failed")

    # Launch Owping (clients) Scheduler
    owamp.start_owping_scheduler(scheduler_callback, scheduler_callback_fail, scheduler_callback_ping_failed)
    print("Dev: Owmping scheduler started..")
    signal.signal(signal.SIGINT, signal_handler)

    # Infinite Loop
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
