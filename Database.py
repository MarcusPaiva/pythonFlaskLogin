import sqlite3


class Database:
	
	def create_connection( self, database_name ):
		"""
		Create connection using SQLite
		"""
		self.conn = sqlite3.connect(database_name,check_same_thread=False,isolation_level=None)
		
	def create_cursor(self):
		"""
		Create a cursor
		"""
		self.cursor = self.conn.cursor()

	def create_table_user(self):
		"""
		Create user's table
		"""
		self.cursor.execute( """Create table if not exists userlogin( 
			id integer primary key,
			username text,
			useremail text,
			userpassword text
		 )""" )

	def add_new_user(self, user_name, user_email, user_password ):
		"""
		Create a new User
		"""
		#check before if email already existis, if true block to create
		if not self.has_email(user_email):
			self.cursor.execute("insert into userlogin(username,useremail,userpassword) values(?,?,?);",
				(user_name,user_email,user_password))
			return self.cursor.lastrowid

	def login(self,user_email,user_password ):
		self.cursor.execute( "select * from userlogin where useremail=? and userpassword=?;",
			(user_email,user_password) )
		return self.cursor.fetchone()

	def has_email( self,user_email ):
		"""
		Check if email already existis
		"""
		self.cursor.execute( "select * from userlogin where useremail=?;", (user_email,) )
		return self.cursor.fetchone()