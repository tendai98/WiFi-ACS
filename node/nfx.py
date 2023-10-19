def host_control(args):

	db = args[0]
	target_node = args[1][0]
	host_table = args[1][1]

	for host in host_table:
		dev_info = host_table[host]
		entry = {'node': target_node, 'id':host, 'data': dev_info}
		db.insert(entry)

