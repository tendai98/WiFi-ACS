from time import sleep
from json import loads
from threading import Thread
from scapy.all import sendp, Dot11, Dot11Deauth, RadioTap

class Layer2Protection:
	__config = None
	__db = None
	def __init__(self, config):
		self.__config = config
		firewall = Thread(target=self.__run, args=(config['target'], config['allowed'], config['blocked']))
		firewall.start()


	def __load_database(self):
		fd = open(self.__config['database'])
		data = fd.read()
		fd.close()
		return loads(data)

	def __block_device(self, target):
		bssid = self.__config['bssid']
		dth = RadioTap()/Dot11(addr1=target, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
		sendp(dth, iface=self.__config['interface'])

	def __run(self, target_table, allowed_table, blocked_table):

		while True:
			try:
				self.__db = self.__load_database()
				targets = self.__db[target_table]
				allowed = [ mac for mac in self.__db[allowed_table] ]
				blocked = [ mac for mac in self.__db[blocked_table] ]

				for target in targets:
					if target not in allowed:
						t = Thread(target=self.__block_device, args=(target,))
						t.start()

				for target in blocked:
						t = Thread(target=self.__block_device, args=(target,))
						t.start()

			except KeyboardInterrupt:
				exit()

			except:
				pass

			sleep(0.1)
