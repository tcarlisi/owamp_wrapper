# OWAMP Wrapper
## Presentation

This is a perfsonar2 OWAMP implementation (https://github.com/perfsonar/owamp) API that let's you create an OWAMP server or ping one. 

The API consists in the following functions:
- configure() : it must be called before every other functions. It's goal is to configure the OWAMP directory using the customizable config.ini file.
- start_server() / stop_server() : start/stop the OWAMP server
- start_owping_scheduler() / stop_owping_scheduler() : start/stop a scheduler to ping the list of address (defined in config.ini) at a wanted frequency

## Installation

- Clone the git 
- install python modules (requirements.txt)
- if Automake is not installed on your machine, do it `sudo apt-get install -y automake` (on Ubunutu)
- run install.sh that will install owamp in the Implemenation/ directory
- You are ready to go

## Use
First, one needs to modify the documented config.ini to choose the parameters you want.
Then one needs to import and use the functions present in the owamp_api.py well documented source file.

# A word on ping interval
The scheduler frequency (ping interval) can be chosen. This value should be higher than the time to realize a ping. AN OWAMP ping is estimated to last : 
    1 + timeout + nb_pkts * send_schedule

If this time is, for example equal to 10 seconds, choose an interval of at least 11 seconds.
