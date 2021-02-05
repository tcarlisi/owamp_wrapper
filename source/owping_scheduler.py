"""
owping_scheduler.py
    Owping scheduler
@author: Thomas Carlisi
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from datetime import datetime
from owamp_client import OwampClient
from owamp_stats import OwampStats


class OwpingScheduler():
    """
    TODO : Doc
    """

    def __init__(self,
                address_list,
                ip_version, 
                nb_packets, 
                schedule,
                authentication,
                port_range,
                dhcp_value):
        self.address_list = address_list
        self.ip_version = ip_version
        self.nb_packets = nb_packets
        self.schedule = schedule
        self.authentication = authentication
        self.port_range = "" if port_range == 0 else port_range
        self.dhcp_value = "" if dhcp_value == 0 else dhcp_value

        self.scheduler = BackgroundScheduler()

        self.owpingers = []

    def start_owping_scheduler(self):
        print("Owmping scheduler started..")
        self.scheduler.start()
        self.scheduler.add_listener(self._scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self._create_owpingers()
        print(len(self.owpingers))
        for owpinger in self.owpingers:
            self.scheduler.add_job(owpinger.owping, trigger="interval", seconds=20, replace_existing=True, next_run_time=datetime.now())

    def shutdown_owping_scheduler(self):
        self.scheduler.shutdown()

    def _scheduler_listener(self, event):
        if event.exception:
            print('The job crashed :(')
        else:
            print('The job worked :)')
            owamp_stats = event.retval
            owamp_stats._debug_print_stats()

    def _create_owpingers(self):

        for addr in self.address_list:
            owpinger = OwampClient(addr, self.ip_version, self.nb_packets,
                self.schedule, self.authentication, self.port_range, 
                self.dhcp_value)

            self.owpingers.append(owpinger)

    