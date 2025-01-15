import pymysql


class ManageDb:
	"""
	数据库基础配置
	"""

	def __init__(self, db, user=None, passwd=None, host=None, port=3306, charset='utf8'):
		self.db = db
		self.user = user
		self.passwd = passwd
		self.host = host
		self.port = port
		self.charset = charset
		self.connect = None
		self.cursor = None

	def connect_db(self):
		"""
		连接数据库和创建游标
		:return:
		"""
		params = {
			"db": self.db,
			"user": self.user,
			"passwd": self.passwd,
			"host": self.host,
			"port": self.port,
			"charset": self.charset
		}
		self.connect = pymysql.connect(**params)
		self.cursor = self.connect.cursor()
		return self.connect

	def close_db(self):
		"""
		关闭数据库和游标
		:return:
		"""
		self.cursor.close()
		self.connect.close()
