from os import system

def start_monitor_interface(interface):
	system("airmon-ng start {}".format(interface))
