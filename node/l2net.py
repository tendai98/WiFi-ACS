from scapy.all import sniff, conf
from threading import Thread
from json import load, dumps
from requests import post
from socket import socket
from time import time, sleep
from os import system as exec


conf.verb = 0
radio = {'channel': 1, 'lock':0}


class Layer2NetOPS:

	mac_table = {}
	ieee = None
	sock = socket(2, 2)
	API_ENDPOINT = ("127.0.0.1", 9393)

	def find_vendor(self, mac):
		parsed_mac = mac.replace(":","").upper()[:6]
		try:
			return self.ieee[parsed_mac]
		except:
			return "N/A"

	def post_data(self, endpoint, json_data):
		data = dumps(json_data)
		self.sock.sendto(data.encode(), endpoint)

	def __run_passive(self, config):

		def packet_handler(packet):

			vendor_id = ''
			mac = ''
			try:
				if packet != None and packet.type == 2:

					mac = packet.addr1
					filter = not (mac == None or mac == 'ff:ff:ff:ff:ff:ff' or '33:33' in mac or '01:00' in mac)
					if(filter and packet.addr2 == config['bssid']):
						if len(self.mac_table) >= int(config['deviceLimit']):
							print("[-] LIMIT_HIT:  Flushing table...")
							self.mac_table = {}

						if (mac not in self.mac_table):
							vendor_id = self.find_vendor(mac)
							self.mac_table.update({ mac:{'vendor': vendor_id, 'timestamp': int(time()) }})
							self.post_data(self.API_ENDPOINT, {'command': 'host-ctl', 'data': ['connected_devices', self.mac_table]})
							print('[+] New device: %s ' % mac)
						else:

							duration = int(config['duration'])
							c_epoch = int(time())
							epoch = self.mac_table[mac]['timestamp']

							if ((c_epoch - epoch) >= duration):
								print("[-] Flushing Out: %s" % mac)
								self.mac_table.pop(mac)
								self.post_data(self.API_ENDPOINT, {'command': 'host-ctl', 'data': ['connected_devices', self.mac_table]})
							else:
								vendor_id = self.find_vendor(mac)
								self.mac_table[mac]['timestamp'] = int(time())
								self.post_data(self.API_ENDPOINT, {'command': 'host-ctl', 'data': ['connected_devices', self.mac_table]})
			except:
				pass

		print("[++] NETSCAN :: [ACTIVE]")
		sniff(iface=config["interface"], prn=packet_handler)

	def __init__(self, config):

		try:
			fd = open(config['ieeeData'])
			self.ieee = load(fd)
			fd.close()
			exec('iwconfig {} channel {}'.format(config['interface'], config['channel']))
			passive_mode = Thread(target=self.__run_passive, args=(config, ))
			passive_mode.start()

		except Exception as e:
			print("[NETSCAN]:: An Error has occured => ({})".format(str(e)))
			print("[--] Execute :: [SHUTDOWN]")
			exit(-1)
