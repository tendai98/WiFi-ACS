import json

DEFAULT_CONFIG = "data/config.json"
HELP_INDEX = "data/help.json"
IEEE_DATA = "data/ieee.json"

current_database = None
database_open = False
database = None

def find_vendor(mac):
	ieee = load(IEEE_DATA)
	parsed_mac = mac.replace(":","").upper()[:6]
	try:
		return ieee[parsed_mac]
	except:
		return "N/A"

def commit(path, data):
	fd = open(path, 'w')
	json.dump(data, fd)
	fd.close()
	print('[+] Data Saved')


def load(path):
	fd = open(path, 'r')
	data = json.load(fd)
	fd.close()
	return data

def add_guest(args):

	global database
	global current_database
	global database_open

	try:
		if database_open:
			try:
				database[args[0]].update({args[1]: {'vendor': find_vendor(args[1]), 'duration':int(args[2])}})
				commit(current_database, database)
				database = load(current_database)
			except:
				print('[!] Exception has occured adding host')
		else:
				print('[!] Load database first')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')

def add_host(args):

	global database
	global current_database
	global database_open

	try:
		if database_open:
			try:
				database[args[0]].update({args[1]: {'vendor': find_vendor(args[1])}})
				commit(current_database, database)
				database = load(current_database)
			except KeyError:
				print('[!] Target host node: Not Found')
		else:
			print('[!] Load database first')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')

def delete_host(args):
	global database
	global database_open
	global current_database

	try:
		if database_open:
			try:
				database[args[0]].pop(args[1])
				commit(current_database, database)
				database = load(current_database)
			except KeyError:
				print('[!] Target host node: Not Found')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')



def list_hosts(args):
	global database
	global database_open

	try:
		if database_open:
			print('Network Node::: %s' % args[0])
			print('\n   [MAC Address]       [Device Vendor]\n')
			for host in database[args[0]]:
				print('   %s   %s' % (host, database[args[0]][host]['vendor']) )
			print('')
		else:
			print('[!] Load database first')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')

def list_nodes(args):
	global database
	global database_open

	try:
		if database_open:
			print("\t\tNetwork Host Nodes")
			for node in database:
				print("\t\t{}:\tHost count:{}".format(node, len(database[node])))
		else:
			print("[!] LOad database first")
	except:
		print('Execution failed: Type "help -a" to get info on commands')

def flush_database(args):

	global database
	global current_database
	global database_open

	try:
		if database_open:
			for node in database:
				database[node] = {}
			commit(current_database, database)
			database = load(current_database)
		else:
			print('[!] Load database first')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')


def open_database(args):

	global current_database
	global database
	global database_open

	try:
		current_database = args[0]
		database = load(args[0])
		database_open = True
		print('[+] Database loaded')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')

def create_node(args):

	global current_database
	global database
	global database_open

	try:
		if database_open:
			database.update({args[0]: {}})
			commit(current_database, database)
			database = load(current_database)
			print('[+] Host node: %s' % args[0])
		else:
			print('[!] Load database first')
	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except Exception:
		print('[!!] Critical Command Error')


def flush_node(args):
	create_node(args)

def sys_config(args):
	try:
		configs = load(DEFAULT_CONFIG)

		if args[0] == '-v':	#View config
			print('   \n[Configuration]    [Value]')
			for key in configs:
				print('   %s:   %s' % (key, configs[key]))
			print('')
		elif args[0] == '-s':	#Set parameter
			configs[args[1]] = args[2]
			commit(DEFAULT_CONFIG,configs)

	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')

def help_cmd(args):
	try:
		index = load(HELP_INDEX)
		if(args[0] == "-a"):
			try:
				print(index['label'])
				index.pop('label')
				for key in index:
					print('\t%s\t%s' % (key, index[key]))
			except KeyError:
				print("[!] Help info for command not found")
		else:
			print("\n%s" % index[args[0]])

	except IndexError:
		print('Execution failed: Type "help -a" to get info on commands')
	except:
		print('[!!] Critical Command Error')
