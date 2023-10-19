import json
from hashlib import md5
from time import sleep as delay


DEFAULT_CONFIG	=	"data/config.json"
HELP_INDEX	=	"data/help.json"
IEEE_INDEX	=	"data/ieee.json"
COMMAND_ERROR_MESSAGE =	"Operation Failed"
AUTH_OK_MESSAGE	=	"Access Granted"
AUTH_ERROR_MESSAGE =	"Invalid Username or Password"
AUTH_FAILED_MESSAGE =	"Operation Not Permitted"

current_database = "data/net.json"
database = None
access = False


def find_vendor(mac):
	ieee = load(IEEE_INDEX)
	parsed_mac = mac.replace(":","").upper()[:6]
	try:
		return ieee[parsed_mac]
	except:
		return "N/A"

def commit(path, data):
	fd = open(path, 'w')
	json.dump(data, fd)
	fd.close()

def load(path):
	fd = open(path, 'r')
	data = json.load(fd)
	fd.close()
	return data

def auth_user(args):
	global access
	try:

		username = args[0]
		password = args[1]
		usr = load(DEFAULT_CONFIG)['username']
		hsh = load(DEFAULT_CONFIG)['password']
		print("[] USER AUTH: EXECUTED")

		if (username == usr and hsh == md5(password.encode()).hexdigest()):
			access = True
			return json.dumps({'message':AUTH_OK_MESSAGE, 'code':0})
		else:
			access = False
			return json.dumps({'message':AUTH_ERROR_MESSAGE, 'code':-1})

	except:
		access = False
		return json.dumps({'message':AUTH_ERROR_MESSAGE, 'code':0})



def add_guest_x(args):
	global access
	global database
	global current_database

	if access:
		try:
			database[args[0]].update({args[1]: {'vendor': find_vendor(args[1]), 'duration':int(args[2])}})
			commit(current_database, database)
			database = load(current_database)
			print("[+] Add Guest User")
			return json.dumps({'message':'Guest host added', 'code':0, 'data': database[args[0]]})
		except Exception as e:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})


def add_host(args):
	global access
	global database
	global current_database

	if access:
		try:
			database[args[0]].update({args[1]: {'vendor': find_vendor(args[1])}})
			commit(current_database, database)
			database = load(current_database)
			print("[+] Add Host Device")
			return json.dumps({'message':'Host added', 'code':0, 'data': database[args[0]]})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})

def delete_host(args):
	global access
	global database
	global current_database

	if access:
		try:
			database[args[0]].pop(args[1])
			commit(current_database, database)
			delay(0.25)
			database = load(current_database)
			print("[+] Host Deleted: "+args[1])
			return json.dumps({'message':'Host deleted', 'code':0, 'data': database[args[0]]})
		except Exception as e:
			print(e)
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})

def list_hosts(args):
	global access
	global database

	if access:
		try:
			return json.dumps({'message':'Listing Hosts', 'code':0, 'data': database[args[0]]})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})

def list_nodes(args):
	global access
	global database

	if access:
		try:
			node_count = {}
			for node in database:
				node_count.update({node: len(database[node])})
			return json.dumps({'message':'Listing Host Nodes', 'code':0, 'data': node_count})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})


def flush_database(args):
	global access
	global database
	global current_database

	if access:
		try:
			for node in database:
				database[node] = {}

			commit(current_database, database)
			database = load(current_database)
			return json.dumps({'message':'Database Flushed', 'code':0, 'data': database})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})

def open_database(args):

	global current_database
	global database
	global access

	if access:
		try:
			current_database = args[0]
			database = load(args[0])
			return json.dumps({'message':'Database loaded', 'code':0})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})


def flush_node(args):

	global current_database
	global database
	global access

	if access:
		try:
			database.update({args[0]: {}})
			commit(current_database, database)
			database = load(current_database)
			return json.dumps({'message':'Flushed Node: %s' % args[0], 'code':0})
		except Exception:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})
	else:
		return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})


def sys_config(args):
	global access

	if access:
		try:
			if args[0] == '-v':

				configs = load(DEFAULT_CONFIG)
				configs.pop("password")
				return json.dumps({'message':'Loading Configurations...', 'code':0, 'data': configs})

			elif args[0] == '-s':
				configs = load(DEFAULT_CONFIG)
				configs[args[1]] = args[2]
				commit(DEFAULT_CONFIG,configs)
				return json.dumps({'message':'Reloading Configurations...', 'code':0, 'data': configs})

			else:
				return json.dumps({'message':AUTH_FAILED_MESSAGE, 'code':-1})
		except:
			return json.dumps({'message':COMMAND_ERROR_MESSAGE, 'code':-1})

