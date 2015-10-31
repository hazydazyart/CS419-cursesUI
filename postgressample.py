import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = None
adminCon = None

def setup_admin_con():
	try:
		adminCon = psycopg2.connect(dbname='postgres' user='postgres')
		adminCon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		
	except psycopg2.DatabaseError, e:
		print 'Error, unable to connect as admin. Admin operations may be unavailable.'
			
# todo: add user perms from checkboxes in form?
def create_user(name):
	try:
		cur = adminCon.cursor()
		cur.execute('CREATE USER ' + name)
		
	except psycopg2.DatabaseError, e:
			if adminCon:
				adminCon.rollback()
		print 'Error, unable to create new user ' + user
	
	print 'Created user ' + name
	
def create_database(dbname, owner):
	try:
		cur = adminCon.cursor()
		cur.execute('CREATE DATABASE ' + name + 'WITH OWNER ' + name)
		
	except psycopg2.DatabaseError, e:
		if adminCon:
			adminCon.rollback()
		print 'Error, unable to create database ' + dbname + ', please try again.'
	
	print 'Created database ' + dbname + ' with owner ' + owner
		
def connect_to_database(dbname, owner):
	try:
		if con:
			con.close()
		con = psycopg2.connect(dbname=dbname user=owner)
		
	except psycopg2.DatabaseError, e:
		print 'Error, unable to connect to database ' + dbname + '.'
		
	print 'Connected to database ' + dbname
	return con

def execute_query(dbname, owner, query):
	try:
		con = connect_to_database(dbname, owner)
		cur = con.cursor()
		cur.execute(query)
		
	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		print 'Error, unable execute query.'
		
	finally:
		if con:
			con.close()
		
		
def create_table_from_form(dbname, owner):

# todo

def create_sample_postgres():
	
	films = (
		(1, 'The Plague of the Zombies', 1966),
		(2, 'White Zombie', 1932),
		(3, 'Warm Bodies', 2013),
		(4, 'Zombieland', 2009),
		(5, 'I Walked with a Zombie', 1943),
		(6, 'Day of the Dead', 1985),
		(7, 'Rec', 2007)
	)

	try:
		cur = adminCon.cursor()
		cur.execute('CREATE DATABASE Movies WITH OWNER postgres')
		sampleCon = psycopg2.connect(dbname='Movies' user='postgres')
		cur = sampleCon.cursor()
		cur.execute('CREATE TABLE Zombie(Id INT PRIMARY KEY, Title TEXT, Year INT)')
		query = 'INSERT INTO Zombie (Id, Title, Year) VALUES (%s, %s, %s)'
		cur.executemany(query, films)
		
	except psycopg2.DatabaseError, e:
		if sampleCon:
			sampleCon.rollback()
		print 'Error creating sample database'
		
	finally:
		if sampleCon:
			sampleCon.close()
			
def select_all_from_table(dbname, owner, table):
	try:
		con = connect_to_database(dbname, owner)
		cur = con.cursor()
		cur.execute('SELECT * FROM ' + table)
		rows = cur.fetchall()
		
		for row in rows:
			print row
			
	except psycopg2.DatabaseError, e:
		print 'Error fetching rows from ' + table
		
	finally:
		if con:
			con.close()
		
		
def list_tables(dbname, owner):
	try:
		con = connect_to_database(dbname, owner)
		cur = con.cursor()
		cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
	   
		rows = cur.fetchall()
	   
		for row in rows:
			print row[0]
		
	except psycopg2.DatabaseError, e:
		print 'Error fetching table names from database ' + dbname
		
	finally:
		if con:
			con.close()
		

def delete_table(dbname, owner, table):
	try:
		con = connect_to_database(dbname, owner)
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXSISTS ' + table)
		
	except psycopg2.DatabaseError, e:
		print 'Unable to delete table ' + table
		
	finally:
		if con:
			con.close()
		