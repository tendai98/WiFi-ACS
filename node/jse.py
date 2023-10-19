from json import load, dump

class JSE:

	db = {}
	dbname = None

	def __start_db(self):
		fd = open(self.dbname, "w")
		dump({}, fd)
		fd.close()


	def __flush_db(self):
		fd = open(self.dbname, "w")
		dump(self.db, fd)
		fd.close()

	def __read_db(self):
		fd = open(self.dbname, "r")
		data = load(fd)
		fd.close()
		return data

	def __commit(self):
		tmp = self.__read_db()
		if tmp != self.db:
			self.__flush_db()
		self.db = self.__read_db()

	def open(self, dbname):
		print("[++] JSE :: [ACTIVE]")
		self.dbname = dbname

		try:
			self.db = self.__read_db()
		except:
			self.__start_db()

	def insert(self, args):
		try:
			self.db[args['node']].update({ args["id"]: args["data"] })
		except:
			self.db.update({args["node"]: {}})
			self.db[args["node"]].update({ args["id"]: args["data"] })
		self.__commit()

	def find_one(self, args):
		try:
			return self.db[args["node"]][args["id"]]
		except:
			return None

	def find_many(self, args):
		try:
			return self.db[args['node']]
		except:
			return None

	def delete(self, args):
		self.db[args["node"]].pop(args["id"])
		self.__commit()

	def flush_node(self, args):
		self.db[args["node"]] = {}
		self.__commit()

	def reset(self):
		self.__start_db()

