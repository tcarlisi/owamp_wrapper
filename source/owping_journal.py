"""
owamp_journal.py
    Owamp Journal
@author: Thomas Carlisi
"""

from collections import defaultdict
from owamp_stats import OwampStats

class OwpingJournal():
    """
    Journalize the statistics from the owpings
    """
    def __init__(self):
        self.journal = defaultdict(list)        # A dictionnary of queues (FIFO) of size 5

    def add_in_journal(self, stats: OwampStats):
        if len(self.journal[stats.address]) >= 5:
            self.journal[stats.address].pop(0)

        self.journal[stats.address].append(stats)
    
    def print_journal(self):
        print(self.journal.items())

