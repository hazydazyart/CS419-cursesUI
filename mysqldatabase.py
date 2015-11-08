import MySQLdb
import sys
import exceptions
import mysql.connector
from mysql.connector import errorcode, MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def connectMySQL():

	db_config = read_db_config()

	try:
#		con = mysql.connector.connect(**db_config)
		con = MySQLConnection(**db_config)

		if con.is_connected():
			print('Connected to MySQL database')
		else:
			print('Unable to connect')

	except Error as error:
		print(error)

	finally:
		con.close()
		print('Connection closed')

#if __name__ == '__main__':
#	connectMySQL()

def createDatabase():

	dbconfig = read_db_config()

	try:
		con = MySQLConnection(**db_config)
		cursor = con.cursor()
		cursor.execute('CREATE DATABASE ' + name + 'WITH OWNER ' + name)

		if con.is_connected():
			print('Connected to MySQL database')
	except Error as error:
		print(error)



def executeQuery():
	try:
		dbconfig = read_db_config()
		con = MySQLConnection(**db_config)
		cursor = con.cursor()
		cursor.execute("SELECT * FROM table")

#		row = cursor.fetchone()
		rows = cursor.fetchall()

#		while row is not None:
#			print(row)
#			row = cursor.fetchone()

		print('Totals Row(s):', cursor.rowcount)
		for row in rows:
			print(row)

	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()


#if __name__ == '__main__':
#	executeQuery()

def insertData():
	query = "INSERT INTO table() " \
			"VALUES()"
	args = ()

	try:
		db_config = read_db_config()
		con = MySQLConnection(**db_config)

		cursor = con.cursor()
		cursor.execute(query, args)

		if cursor.lastrowid:
			print('last insert id', cursor.lastrowid)
		else:
			print('last insert id not found')

		con.commit()
	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()


#if __name__ == '__main__':
#	insertData()

def updateData(arg1, arg2):

	db_config = read_db_config()

	query = """ UPDATE table
				SET arg2 = %s
				WHERE arg1 = %s"""

	data = (arg2, arg1)

	try:
		con = MySQLConnection(**db_config)

		cursor = con.cursor()
		cursor.execute(query, data)

		con.commit()

	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()

#if __name__ == '__main__':
#	updateData(arg1, arg2)

def deleteData():
	db_config = read_db_config()

	query = "DELETE FROM table WHERE id = %s"

	try:
		con = MySQLConnection(**db_config)

		cursor = con.cursor()
		cursor.execute(query, (table_id,))

		con.commit()

	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()

#if __name__ == '__main__':
#	deleteData(table_id)


def listTables():
	db_config = read_db_config()

	query = "SELECT table_name FROM database WHERE"

	try:
		con = MySQLConnection(**db_config)	
		
		cursor = con.cursor()
		cursor.execute(query)

		rows = cursor.fetchall()

		for row in rows:
			print row[0]

	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()


def deleteTable():

	db_config = read_db_config()

	query = 'DROP TABLE IF EXISTS ' + table)

	try:
		con = MySQLConnection(**db_config)
		cursor = con.cursor()
		cursor.execute(query)

	except Error as error:
		print(error)

	finally:
		cursor.close()
		con.close()

def createTable():