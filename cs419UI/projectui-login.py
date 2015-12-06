import npyscreen
import curses
import psycopg2
import mysql.connector
import csv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from mysql.connector import errors

### PostgreSQL connection variables

psqlCon = None
psqlAdmin = None

### PostgreSQL user info variables
psqlName = None
psqlUser = None
psqlPass = None
psqlHost = None
psqlPort = None

#Main form manager
class projectApp(npyscreen.NPSAppManaged):
    def onStart(self):
    	self.addForm('MAINOPT', MainOpt)  
    	self.addForm('MAIN', MainLogin, name="Project UI")
	self.addForm('ROOTMENU', RootMenu) 
	self.addForm('ADMINMENU', AdminMenu)
    	self.addForm('CREATEDB', CreateDB)
    	self.addForm('SQLQRY', SQLQuery)
	self.addForm('USERINFO', UserInfo)
    	self.addForm('VIEWTB', BrowseTable)
    	self.addForm('DELETEDB', DeleteDB)
    	self.addForm('IMPORTDB', ImportDB)
    	self.addForm('EXPORTDB', ExportDB)
    	self.addForm('FAQ', FAQ)

			
class ConnectToPostgres(npyscreen.ButtonPress):
	def whenPressed(self):
		global psqlHost
		global psqlPort
		global psqlName
		global psqlPass
		global psqlUser
		
		#get values from form
		psqlHost = self.parent.get_widget('host').value
		psqlPort = self.parent.get_widget('port').value
		psqlName = self.parent.get_widget('name').value
		psqlUser = self.parent.get_widget('user').value
		psqlPass = self.parent.get_widget('pass').value
		
		#try to connect
		try:
			global psqlCon
			
			psqlCon = psycopg2.connect(database=psqlName, user=psqlUser, password=psqlPass, host=psqlHost, port=psqlPort)
			psqlCon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
			
		except psycopg2.DatabaseError, e:
			msg = 'Error %s' % e
			npyscreen.notify_confirm(msg)
			return

		try:
			global psqlAdmin
			psqlAdmin = psycopg2.connect(database='postgres', user='postgres')
			psqlAdmin.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		
		except psycopg2.DatabaseError, e:
			npyscreen.notify_confirm('Unable to connect to administrator database. Administration functions may not be available.')
			
		self.parent.goToMain()

#Show signed in user's information
class MainLogin(npyscreen.Form):
	
	def create(self):
		msg1 = "Sign into an existing PostgreSQL database"
		msg2 = "*Required for non-local databases"
		self.add(npyscreen.TitleFixedText, name = msg1)
		self.add(npyscreen.TitleText, name = "Database name:", w_id="name", value = "movies")
		self.add(npyscreen.TitleText, name = "Username:", w_id="user", value = "postgres")
		self.add(npyscreen.TitleText, name = "Password:", w_id="pass", value = "postgres")
		self.add(npyscreen.TitleText, name = "Host:", w_id="host", value = "0.0.0.0")
		self.add(npyscreen.TitleText, name = "Port:", w_id="port", value = "5432")
		self.add(ConnectToPostgres, name = "Connect to Database")

	# return to login options screen
	def on_ok(self):
		self.parentApp.switchForm('MAIN')
		
	def goToMain(self, *args, **keywords):
		self.parentApp.switchForm('MAINOPT')

#Main Screen + Menu
class MainOpt(npyscreen.FormBaseNewWithMenus):

	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Welcome! To get started, select an option from the menu." )
		self.menu = self.add_menu(name="Main Menu", shortcut="^M")
		self.menu.addItem(text="Enter a Query", onSelect=self.SQLQuery)
		self.menu.addItem(text="Browse a Table", onSelect=self.BrowseTable)
		self.menu.addItem(text="Administration", onSelect=self.AdminMenu)
		self.menu.addItem(text="Export Table Data", onSelect=self.exDB)
		self.menu.addItem(text="Import Table Data", onSelect=self.impDB)
		self.menu.addItem(text="FAQ", onSelect=self.showFAQ)
		self.menu.addItem(text="Switch Databases", onSelect=self.switch)
		self.menu.addItem(text="Exit", onSelect=self.exit)
	
	def AdminMenu(self):
		self.parentApp.switchForm('ADMINMENU')
	
	def SQLQuery(self):
		self.parentApp.switchForm('SQLQRY')
		
	def BrowseTable(self):
		self.parentApp.switchForm('VIEWTB')
		
	def modDB(self):
		self.parentApp.switchForm('EDITDB')
	
	def exDB(self):
		self.parentApp.switchForm('EXPORTDB')
	
	def impDB(self):
		self.parentApp.switchForm('IMPORTDB')
	
	def showFAQ(self):
		self.parentApp.switchForm('FAQ')
	
	def switch(self):
		self.parentApp.switchForm('MAIN')
		
	def exit(self):
		self.parentApp.switchForm(None)

#Main Screen + Menu MYSQL
class MyMainOpt(npyscreen.FormBaseNewWithMenus):

	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select an option from the menu below for MySQL." )
		self.menu = self.add_menu(name="Main Menu", shortcut="^M")
		self.menu.addItem(text="User Information", onSelect=self.Myshowinfo)
#		self.menu.addItem(text="Add PostgreSQL Database", onSelect=self.MyaddDB)
#		self.menu.addItem(text="View PostgreSQL Databases", onSelect=self.MylistDB)
		self.menu.addItem(text="Enter a Query", onSelect=self.MySQLQuery)
		self.menu.addItem(text="Browse a Table", onSelect=self.MyBrowseTable)
		self.menu.addItem(text="Administration", onSelect=self.RootMenu)
#		self.menu.addItem(text="Create & Modify Databases", onSelect=self.MymodDB)
#		self.menu.addItem(text="Query Databases", onSelect=self.MyqueryDB)
#		self.menu.addItem(text="Import a Database", onSelect=self.MyexDB)
#		self.menu.addItem(text="Export a Database", onSelect=self.MyimpDB)
#		self.menu.addItem(text="FAQ", onSelect=self.MyshowFAQ)
		self.menu.addItem(text="Exit", onSelect=self.Myexit)
	
	def RootMenu(self):
		self.parentApp.switchForm('ROOTMENU')
		
	def Myshowinfo(self):
		self.parentApp.switchForm('MYUSERINFO')
	
	def MySQLQuery(self):
		self.parentApp.switchForm('MYSQLQRY')
		
	def MyBrowseTable(self):
		self.parentApp.switchForm('MYVIEWTB')
		
	def MymodDB(self):
		self.parentApp.switchForm('MYEDITDB')
	
	def MyqueryDB(self):
		self.parentApp.switchForm('MYQRYDB')
	
	def MyexDB(self):
		self.parentApp.switchForm('MYEXPORTDB')
	
	def MyimpDB(self):
		self.parentApp.switchForm('MYIMPORTDB')
	
	def MyshowFAQ(self):
		self.parentApp.switchForm('MYFAQ')
	
	def Myexit(self):
		self.parentApp.switchForm(None)

### BEGIN POSTGRES
class AdminMenu(npyscreen.Form):
	def create(self):
		self.add(AdminCreateDatabaseForm, name="Create a Database")
		self.add(AdminDeleteDatabaseForm, name="Delete a Database")
		self.add(AdminViewUsersForm, name="View Users")
		
	def goToCreate(self, *args, **keywords):
		self.parentApp.switchForm('CREATEDB')
		
	def goToDelete(self, *args, **keywords):
		self.parentApp.switchForm('DELETEDB')
		
	def goToUsers(self, *args, **keywords):
		self.parentApp.switchForm('USERINFO')

	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class AdminCreateDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToCreate()

class AdminDeleteDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToDelete()
		
class AdminViewUsersForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToUsers()
		
class UserInfo(npyscreen.Form):
	def create(self):
		self.add(FetchUsersButton, name="Press to Fetch User Information")
		self.add(npyscreen.GridColTitles, name="Users:", w_id="viewusers", max_height=7, scroll_exit=True)
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
# Command to fetch user info from http://www.postgresql.org/message-id/1121195544.8208.242.camel@state.g2switchworks.com
class FetchUsersButton(npyscreen.ButtonPress):
	def whenPressed(self):
		try:
			global psqlAdmin
			cur = psqlAdmin.cursor()
			cmd = """SELECT u.usename AS "User name", u.usesysid AS "User ID", CASE WHEN u.usesuper AND u.usecreatedb THEN CAST('superuser, create database' AS pg_catalog.text) WHEN u.usesuper THEN CAST('superuser' AS pg_catalog.text) WHEN u.usecreatedb THEN CAST('create database' AS pg_catalog.text) ELSE CAST('' AS pg_catalog.text) END AS "Attributes" FROM pg_catalog.pg_user u ORDER BY 1;"""
			cur.execute(cmd)
			output = []
			cols = [cn[0] for cn in cur.description]
			output.append(cols)
			rows = cur.fetchall()
			for row in rows:
				output.append(row)
			self.parent.get_widget('viewusers').values = output
			self.parent.get_widget('viewusers').display()
		except psycopg2.DatabaseError, e:
			if psqlAdmin:
				psqlAdmin.rollback()
			npyscreen.notify_confirm('Could not fetch user info: %s' % e)
		return
		
class CreateDB(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Add a PostgreSQL Database")
		self.dbname = self.add(npyscreen.TitleText, name = "Database name: ")
		self.owner = self.add(npyscreen.TitleText, name = "Owner name: ")
		
	def beforeEditing(self):
		self.dbname.value = ''
		self.owner.value = ''
		
	def afterEditing(self):
		name = self.dbname.value
		owner = self.owner.value
		msg = createPsqlDB(name, owner)
		npyscreen.notify_confirm(msg)
		self.parentApp.switchFormPrevious()
		
class DeleteDB(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Delete a Database")
		self.add(FetchDbsButton, name="Refresh Database Names")
		self.add(npyscreen.TitleSelectOne, name="Databases:", w_id="dmenu", max_height=5, scroll_exit=True)
		self.add(DeleteDbButton, name="Delete Selected Database")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class FetchDbsButton(npyscreen.ButtonPress):
	def whenPressed(self):
		try:
			global psqlAdmin
			cur = psqlAdmin.cursor()
			cur.execute("SELECT datname FROM pg_database")
			rows = cur.fetchall()
			output = []
			for row in rows:
				output.append(row)
			self.parent.get_widget('dmenu').values = [val[0] for val in output]
			self.parent.get_widget('dmenu').display()
		except psycopg2.DatabaseError, e:
			if psqlAdmin:
				psqlAdmin.rollback()
			npyscreen.notify_confirm('Could not fetch database names: %s' % e)
		return
		
class DeleteDbButton(npyscreen.ButtonPress):
	def whenPressed(self):
		selected = self.parent.get_widget('dmenu').get_selected_objects()
		try:
			global psqlAdmin
			cur = psqlAdmin.cursor()
			query = "DROP DATABASE " + str(selected[0])
			cur.execute(query)
			
		except psycopg2.DatabaseError, e:
			if psqlAdmin:
				psqlAdmin.rollback()
			npyscreen.notify_confirm('Error dropping database: %s' % e)
			return
		npyscreen.notify_confirm('Successfully dropped database')
		return

#Show create a new database or select a database to modify
class EditDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleText, name = "Create: ", value="New Database")
		grid = self.add(npyscreen.GridColTitles)
		
		grid.col_titles=("col1", "col2", "col3", "col4")
		grid.values = []
		
		for x in range(3):
			row = []
        	for y in range(4):
        		row.append("x: " + str(x) + " y: "+ str(y))
        	
        	grid.values.append(row)
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

#Export a table
class ExportDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Export a Table")
		self.add(FetchTablesButton, name="Refresh table names")
		self.add(npyscreen.TitleSelectOne, name="Tables:", w_id="tmenu", max_height=5, scroll_exit=True)
		self.add(BrowseTableButton, name="Browse Table")
		self.add(npyscreen.BoxTitle, name="All data in table", w_id="tdata", max_height=7, scroll_exit=True)
		
		self.add(npyscreen.TitleFixedText, name="Enter the table name to export")
		self.add(npyscreen.TitleText, name = "Table:", w_id="tblname", value = "")
		self.add(ExportTablesButton, name="Export")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

#Export process referenced from: http://zetcode.com/db/postgresqlpythontutorial/
class ExportTablesButton(npyscreen.ButtonPress):
	def whenPressed(self):
		expTable = self.parent.get_widget('tblname').value
		
		f = None
		
		try:
			global psqlCon
			cur = psqlCon.cursor()
			
			f = open(expTable, 'w')
			cur.copy_to(f, expTable, sep=",")

		except psycopg2.DatabaseError, e:
			npyscreen.notify_confirm("Database Error!")
		
		except IOError, e:
			npyscreen.notify_confirm("Export Error!")
			print 'Error %s' % e
			sys.exit(1)
		
		finally:
			npyscreen.notify_confirm("Successfully Exported %s" % expTable)
			if f:
				f.close()

#Import a table
class ImportDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Import a Table")
		self.add(npyscreen.TitleFixedText, name="***Note***", value="There must be a table to import the data into.")
		self.add(npyscreen.TitleFixedText, name="**********", value="Go to the 'Enter a Query' page to create a table")
		self.add(npyscreen.TitleFixedText, name="Step 1", value="Enter the name of the table to import data into:")
		self.add(npyscreen.TitleText, name = "Table Name:", w_id="imptblname", value = "")
		self.add(npyscreen.TitleFixedText, name="Step 2", value="Enter the name of the file to import data from:")
		self.add(npyscreen.TitleText, name = "File Name:", w_id="impfilename", value = "")
		self.add(ImportTablesButton, name="Import")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

#Import process referenced from: http://zetcode.com/db/postgresqlpythontutorial/
class ImportTablesButton(npyscreen.ButtonPress):
	def whenPressed(self):
		impFile = self.parent.get_widget('impfilename').value
		impTable = self.parent.get_widget('imptblname').value
		
		fopen = None
		
		try:
			global psqlCon
			cur = psqlCon.cursor()
			
			f = open(impFile, 'r')
			cur.copy_from(f, impTable, sep=",")
			psqlCon.commit()

		except psycopg2.DatabaseError, e:
		
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm("Database Error!")
		
		except IOError, e:
		
			if psqlCon:
				psqlCon.rollback()
				
			npyscreen.notify_confirm("Import Error!")
		
		finally:
			npyscreen.notify_confirm("Successfully Imported from file: %s" % impFile)
			if f:
				f.close()
#Show FAQs
class FAQ(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "FAQ")
		howtoq = ["To execute a query, press ^X to access the menu and select 'Enter a Query'.", "From there, you may enter one query at a time in the text box provided.", "Feedback will appear in the second text box.", "If a SELECT statement was entered, the requested values will be printed;", "if INSERT or DELETE queries were entered, a SUCCESS or FAILURE message", "(with reason for failure) will be displayed instead.", "If your user account does not have the appropriate privileges,", "you may be unable to execute your query successfully."]
		self.add(npyscreen.TitleFixedText, name = "How to execute a query")
		for line in howtoq:
			self.add(npyscreen.FixedText, value=line)
		
		howtoswitch = ["To log out of a database, press ^X to access the menu and select", "'Switch Databases'. You will be returned to the login screen,", "where you may re-enter your login credentials", "to log into a different database."]
		self.add(npyscreen.TitleFixedText, name = "How to log in to a different database")
		for line in howtoswitch:
			self.add(npyscreen.FixedText, value=line)
			
		howtoadmin = ["To perform administrator functions, press ^X to access the menu", "and select 'Administration'. This will bring up the administration submenu,", "where databases may be created or deleted,", "and a list of users viewed. The list of users will vary", "based on which database has the active connection."]
		self.add(npyscreen.TitleFixedText, name = "How to perform administration")
		for line in howtoadmin:
			self.add(npyscreen.FixedText, value=line)
			
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
#Execute a query
class SQLQuery(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Enter a Query")
		self.add(npyscreen.MultiLineEditableBoxed, w_id="query", max_height=5, max_width=50, scroll_exit=True)
		self.add(ExecuteQueryButton, name="Execute query")
		self.add(npyscreen.TitleFixedText, name="Query results below:")
		self.add(npyscreen.BoxTitle, w_id="resultstable", max_height=10, max_width=50, scroll_exit=True)
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class ExecuteQueryButton(npyscreen.ButtonPress):
	def whenPressed(self):
		queries = self.parent.get_widget('query').values
		
		try:
			global psqlCon
			cur = psqlCon.cursor()
			for query in queries:
				cur.execute(query)
			psqlCon.commit()
			
			#If command was select, display the data
			command = cur.query.partition(' ')[0]
			if(command == "SELECT"):
				rows = cur.fetchall()
				self.parent.get_widget('resultstable').values = rows
				self.parent.get_widget('resultstable').display()
			elif (command == "DROP"):
				npyscreen.notify_confirm("Table dropped successfully.")
			else:
				output = []
				output.append(cur.query)
				output.append("SUCCESS")
				self.parent.get_widget('resultstable').values = output
				self.parent.get_widget('resultstable').display()

		except psycopg2.DatabaseError, e:
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm("Error executing query!")	
#Get all values from table
class BrowseTable(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Browse a Table")
		self.add(FetchTablesButton, name="Refresh table names")
		self.add(npyscreen.TitleSelectOne, name="Tables:", w_id="tmenu", max_height=5, scroll_exit=True)
		self.add(BrowseTableButton, name="Browse Table")
		self.add(npyscreen.BoxTitle, name="All data in table", w_id="tdata", max_height=7, scroll_exit=True)
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class FetchTablesButton(npyscreen.ButtonPress):
	def whenPressed(self):
		try:
			global psqlCon
			cur = psqlCon.cursor()
			cur.execute("""SELECT table_name from information_schema.tables WHERE table_schema = 'public'""")
			rows = cur.fetchall()
			output = []
			for row in rows:
				output.append(row)
			self.parent.get_widget('tmenu').values = [val[0] for val in output]
			self.parent.get_widget('tmenu').display()
		except psycopg2.DatabaseError, e:
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm('Could not fetch table names.')
		return
		
class BrowseTableButton(npyscreen.ButtonPress):
	def whenPressed(self):
		selected = self.parent.get_widget('tmenu').get_selected_objects()
		try:
			global psqlCon
			cur = psqlCon.cursor()
			query = "SELECT * FROM " + str(selected[0])
			cur.execute(query)
			output = []
			cols = [cn[0] for cn in cur.description]
			output.append(cols)
			rows = cur.fetchall()
			for row in rows:
				output.append(row)
			self.parent.get_widget('tdata').values = output
			self.parent.get_widget('tdata').display()
			
		except psycopg2.DatabaseError, e:
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm('Error fetching data from table')
		return
	
def createPsqlDB(dbname, owner):
	global psqlAdmin
	msg = 'Successfully created database ' + dbname
	try:
		cur = psqlAdmin.cursor()
		command = "CREATE DATABASE " + dbname + " WITH OWNER " + owner
		cur.execute(command)
	except psycopg2.DatabaseError, e:
		if psqlAdmin:
			psqlAdmin.rollback()
		msg = 'Error creating database: %s' % e
	return msg

if __name__ == '__main__':
    PA = projectApp()
    PA.run()
