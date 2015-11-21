import npyscreen
import curses
import psycopg2
import mysql.connector
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

### MySQL Connection variables

mysqlCon = None

### MySQL user variables

mysqlDbase = None
mysqlUser = None
mysqlPass = None
mysqlHost = None

#Main form manager
class projectApp(npyscreen.NPSAppManaged):
    def onStart(self):
    	self.addForm('MAINOPT', MainOpt) 
    	self.addForm('MYMAINOPT', MyMainOpt) #
    	self.addForm('MAIN', MainLogin, name="Project UI")
    	self.addForm('MYSQL', Mysqlf) #
    	self.addForm('POSTGRESQL', Postgref)
    	self.addForm('USERINFO', UserInfo)
    	self.addForm('MYUSERINFO', MyUserInfo) #
	self.addForm('ROOTMENU', RootMenu) #
    	self.addForm('MYCREATEDB', MyCreateDB) #
    	self.addForm('MYSQLQRY', MySQLQuery) #
    	self.addForm('MYVIEWTB', MyBrowseTable) #
    	self.addForm('MYDELETEDB', MyDeleteDB) #
    	self.addForm('MYQRYDB', MyQryDB) #
    	self.addForm('MYIMPORTDB', MyImportDB) #
    	self.addForm('MYEXPORTDB', MyExportDB) #
    	self.addForm('MYFAQ', MyFAQ) #
	self.addForm('ADMINMENU', AdminMenu)
    	self.addForm('CREATEDB', CreateDB)
    	self.addForm('SQLQRY', SQLQuery)
    	self.addForm('VIEWTB', BrowseTable)
    	self.addForm('DELETEDB', DeleteDB)
    	self.addForm('QRYDB', QryDB)
    	self.addForm('IMPORTDB', ImportDB)
    	self.addForm('EXPORTDB', ExportDB)
    	self.addForm('FAQ', FAQ)

#Select DB Type Screen
class MainLogin (npyscreen.Form):
		
	def create(self):
		msg = "Select a database type"
		self.add(npyscreen.TitleFixedText, name = msg)
		self.ch = self.add(npyscreen.TitleSelectOne, max_height=4, value=[0,], name="Select",
			values = ["MySQL", "PostgreSQL"], scroll_exit=True)

	def afterEditing(self):
		
		selectedOpt = str(self.ch.values[self.ch.value[0]])
		
		if selectedOpt == 'MySQL':
			self.parentApp.switchForm('MYSQL')
		
		elif selectedOpt == 'PostgreSQL':
			self.parentApp.switchForm('POSTGRESQL')
			
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
			npyscreen.notify_confirm('Unable to connect to administration database. Administration functions may not be available.')
			
		self.parent.goToMain()

class ConnectToMysql(npyscreen.ButtonPress):
	def whenPressed(self):
		global mysqlHost
		global mysqlDbase
		global mysqlPass
		global mysqlUser
		
		#get values from form
		mysqlHost = self.parent.get_widget('host').value
		mysqlUser = self.parent.get_widget('user').value
		mysqlDbase = self.parent.get_widget('dbase').value
		mysqlPass = self.parent.get_widget('pass').value
		
		#try to connect
		try:
			global mysqlCon
			
			#mysqlCon = mysql.connector.connect(host='localhost', database='mysql', user='root', password='mysql')
			mysqlCon = mysql.connector.connect(host=mysqlHost, database=mysqlDbase, user=mysqlUser, password=mysqlPass)

			if mysqlCon.is_connected():
				print('Connected to MySQL database')
			
		except errors as e:
			npyscreen.notify_confirm('Connection error. Please try again')
			return
		
		self.parent.goToMainMy()

#Show signed in user's information
class Postgref(npyscreen.Form):
	
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

#Show signed in user's information
class Mysqlf(npyscreen.Form):
	
	def create(self):
		msg1 = "Sign into an existing MySQL database or create a new account."
		msg2 = "*Required for non-local databases"
		self.add(npyscreen.TitleFixedText, name = msg1)
		self.add(npyscreen.TitleText, name = "Username:", w_id="user", value= "root")
		self.add(npyscreen.TitleText, name = "Password:", w_id="pass", value= "mysql")
		self.add(npyscreen.TitleText, name = "* Host:", w_id="host", value= "localhost")
		self.add(npyscreen.TitleText, name = "* Database:", w_id="dbase", value= "mysql")
		self.add(npyscreen.TitleFixedText, name = msg2)
		self.add(ConnectToMysql, name = "Connect to Database")
	
	def on_ok(self):
		self.parentApp.switchForm('MYMAIN')

	def goToMainMy(self, *args, **keywords):
		self.parentApp.switchForm('MYMAINOPT')
		
#Main Screen + Menu
class MainOpt(npyscreen.FormBaseNewWithMenus):

	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select an option from the menu below." )
		self.menu = self.add_menu(name="Main Menu", shortcut="^M")
		self.menu.addItem(text="User Information", onSelect=self.showinfo)
#		self.menu.addItem(text="Add PostgreSQL Database", onSelect=self.addDB)
#		self.menu.addItem(text="View PostgreSQL Databases", onSelect=self.listDB)
		self.menu.addItem(text="Enter a Query", onSelect=self.SQLQuery)
		self.menu.addItem(text="Browse a Table", onSelect=self.BrowseTable)
		self.menu.addItem(text="Administration", onSelect=self.AdminMenu)
#		self.menu.addItem(text="Create & Modify Databases", onSelect=self.modDB)
#		self.menu.addItem(text="Query Databases", onSelect=self.queryDB)
#		self.menu.addItem(text="Import a Database", onSelect=self.impDB)
		self.menu.addItem(text="Export a Database", onSelect=self.exDB)
#		self.menu.addItem(text="FAQ", onSelect=self.showFAQ)
		self.menu.addItem(text="Exit", onSelect=self.exit)
	
	def AdminMenu(self):
		self.parentApp.switchForm('ADMINMENU')
		
	def showinfo(self):
		self.parentApp.switchForm('USERINFO')
	
	def SQLQuery(self):
		self.parentApp.switchForm('SQLQRY')
		
	def BrowseTable(self):
		self.parentApp.switchForm('VIEWTB')
		
	def modDB(self):
		self.parentApp.switchForm('EDITDB')
	
	def queryDB(self):
		self.parentApp.switchForm('QRYDB')
	
	def exDB(self):
		self.parentApp.switchForm('EXPORTDB')
	
	def impDB(self):
		self.parentApp.switchForm('IMPORTDB')
	
	def showFAQ(self):
		self.parentApp.switchForm('FAQ')
	
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
#Show signed in user's information
class UserInfo(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Name:", value="John Johnson")
		self.add(npyscreen.TitleFixedText, name = "Role:", value="User")
		self.add(npyscreen.TitleFixedText, name = "Number of Databases", value="2")
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class AdminMenu(npyscreen.Form):
	def create(self):
		self.add(AdminCreateDatabaseForm, name="Create a Database")
		self.add(AdminDeleteDatabaseForm, name="Delete a Database")
		
	def goToCreate(self, *args, **keywords):
		self.parentApp.switchForm('CREATEDB')
		
	def goToDelete(self, *args, **keywords):
		self.parentApp.switchForm('DELETEDB')

	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class AdminCreateDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToCreate()

class AdminDeleteDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToDelete()
		
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
			global psqlCon
			cur = psqlCon.cursor()
			cur.execute("SELECT datname FROM pg_database")
			rows = cur.fetchall()
			output = []
			for row in rows:
				output.append(row)
			self.parent.get_widget('dmenu').values = [val[0] for val in output]
			self.parent.get_widget('dmenu').display()
		except psycopg2.DatabaseError, e:
			if psqlCon:
				psqlCon.rollback()
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

#Select a database to run queries against
class QryDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select a dabase to run queries against")
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

#Import a database
class ImportDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Import a database")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
	
#Export a database
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

class ExportTablesButton(npyscreen.ButtonPress):
	def whenPressed(self):
		expTable = self.parent.get_widget('tblname').value
		
		f = None
		
		try:
			global psqlCon
			cur = psqlCon.cursor()
			
			f = open(expTable, 'r')
			cur.copy_from(f, expTable, sep=",")
			psqlCon.commit()

		except psycopg2.DatabaseError, e:
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm("Database Error!")
		
		except IOError, e:
			if psqlCon:
				psqlCon.rollback()
			npyscreen.notify_confirm("Export Error!")
		
		finally:
			if f:
				f.close()

#Show FAQs
class FAQ(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Show FAQs here")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
#Show Postgres Database names
class ListDB(npyscreen.Form):
	def create(self):
		databases = getDatabaseNames()
		self.add(npyscreen.TitleFixedText, name="List of Postgres Databases")
		grid = self.add(npyscreen.GridColTitles)
		grid.col_titles=("Name")
		grid.values = databases
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
	
#PostgreSQL functions
def getDatabaseNames():
	con = None
	rows = []
	try:
		con = psycopg2.connect(dbname="postgres", user="postgres")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		command = "SELECT datname FROM pg_database"
		cur.execute(command)
		rows = cur.fetchall()
	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		print "Error listing databases " + e
	finally:
		if con:
			con.close()
		return rows

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

### END POSTGRES


### BEGIN MYSQL

#Show signed in user's information
class MyUserInfo(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Name:", value="Root")
		self.add(npyscreen.TitleFixedText, name = "Role:", value="User")
		self.add(npyscreen.TitleFixedText, name = "Number of Databases", value="2")
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class RootMenu(npyscreen.Form):
	def create(self):
		self.add(RootCreateDatabaseForm, name="Create a Database")
		self.add(RootDeleteDatabaseForm, name="Delete a Database")
		
	def goToCreate(self, *args, **keywords):
		self.parentApp.switchForm('MYCREATEDB')
		
	def goToDelete(self, *args, **keywords):
		self.parentApp.switchForm('MYDELETEDB')

	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class RootCreateDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToCreate()

class RootDeleteDatabaseForm(npyscreen.ButtonPress):
	def whenPressed(self):
		self.parent.goToDelete()
		
class MyCreateDB(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Create a new Database")
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class MyDeleteDB(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Delete a Database")
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

#Show create a new database or select a database to modify
class MyEditDB(npyscreen.Form):
	
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

#Select a database to run queries against
class MyQryDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select a dabase to run queries against")
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

#Import a database
class MyImportDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Import a database")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

#Export a database
class MyExportDB(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select a database to export")
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

#Show FAQs
class MyFAQ(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Show FAQs here")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
#Create MySQL database
class MyAddDB(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Add a MySQL Database")
		self.dbname = self.add(npyscreen.TitleText, name = "Database name: ")
		self.owner = self.add(npyscreen.TitleText, name = "Owner name: ")
		
	def beforeEditing(self):
		self.dbname.value = ''
		self.owner.value = ''
		
	def afterEditing(self):
		name = self.dbname.value
		owner = self.owner.value
		msg = MycreateDB(name, owner)
		npyscreen.notify_confirm(msg)
		self.parentApp.switchFormPrevious()

#Show Mysql Database names
class MyListDB(npyscreen.Form):
	def create(self):
		databases = getDatabaseNames()
		self.add(npyscreen.TitleFixedText, name="List of MySQL Databases")
		grid = self.add(npyscreen.GridColTitles)
		grid.col_titles=("Name")
		grid.values = databases
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
#Execute a query
class MySQLQuery(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Enter a Query")
		self.add(npyscreen.MultiLineEditableBoxed, w_id="query", max_height=5, max_width=50, scroll_exit=True)
		self.add(MyExecuteQueryButton, name="Execute query")
		self.add(npyscreen.TitleFixedText, name="Query results below:")
		self.add(npyscreen.BoxTitle, w_id="resultstable", max_height=10, max_width=50, scroll_exit=True)
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

class MyExecuteQueryButton(npyscreen.ButtonPress):
	def whenPressed(self):
		queries = self.parent.get_widget('query').values
		
		try:
			global mysqlCon
			cur = mysqlCon.cursor()
			for query in queries:
				cur.execute(query)
#			mysqlCon.commit()
			
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

		except errors as e:
			if mysqlCon:
				mysqlCon.rollback()
			npyscreen.notify_confirm("Error executing query!")	
#Get all values from table
class MyBrowseTable(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Browse a Table")
		self.add(MyFetchTablesButton, name="Refresh table names")
		self.add(npyscreen.TitleSelectOne, name="Tables:", w_id="tmenu", max_height=5, scroll_exit=True)
		self.add(MyBrowseTableButton, name="Browse Table")
		self.add(npyscreen.BoxTitle, name="All data in table", w_id="tdata", max_height=7, scroll_exit=True)
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
class MyFetchTablesButton(npyscreen.ButtonPress):
	def whenPressed(self):
		try:
			global mysqlCon
			cur = mysqlCon.cursor()
			cur.execute("""SELECT table_name from information_schema.tables WHERE table_schema = 'public'""")
			rows = cur.fetchall()
			output = []
			for row in rows:
				output.append(row)
			self.parent.get_widget('tmenu').values = [val[0] for val in output]
			self.parent.get_widget('tmenu').display()
		except errors as e:
			if mysqlCon:
				mysqlCon.rollback()
			npyscreen.notify_confirm('Could not fetch table names.')
		return
		
class MyBrowseTableButton(npyscreen.ButtonPress):
	def whenPressed(self):
		selected = self.parent.get_widget('tmenu').get_selected_objects()
		try:
			global mysqlCon
			cur = mysqlCon.cursor()
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
			
		except errors as e:
			if mysqlCon:
				mysqlCon.rollback()
			npyscreen.notify_confirm('Error fetching data from table')
		return
		
#MYSQL functions
def MygetDatabaseNames():
	con = None
	rows = []
	try:
		con = mysql.connector.connect(dbname="mysql", user="mysql")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		command = "SELECT datname FROM pg_database"
		cur.execute(command)
		rows = cur.fetchall()
	except errors as e:
		if con:
			con.rollback()
		print "Error listing databases " + e
	finally:
		if con:
			con.close()
		return rows

def MycreateDB(dbname, owner):
	con = None
	msg = 'Successfully created database ' + dbname
	try:
		con = mysql.connector.connect(dbname="mysql", user="mysql")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		command = "CREATE DATABASE " + dbname + " WITH OWNER " + owner
		cur.execute(command)
		rows = cur.fetchall()
	except errors as e:
		if con:
			con.rollback()
		msg = 'Error creating database, ' + e
	finally:
		if con:
			con.close()
		return msg
		
def MyselectAll(table):
	global mysqlCon
	output = []
	try:
		cur = mysqlCon.cursor()
		cur.execute("SELECT * FROM action")
		values = cur.fetchall()
		for row in values:
			output.append(row)
	except errors as e:
		if mysqlCon:
			mysqlCon.rollback()
		print "Error fetching data"
	finally:
		return output
		
def MyexecuteQuery(query):
	global mysqlCon
	msg = 'Successfully executed query!'
	try:
		cur = mysqlCon.cursor()
		cur.execute(query)
	except errors as e:
		if mysqlCon:
			mysqlCon.rollback()
		msg = 'Error: %s ' % e
	finally:
		return msg

if __name__ == '__main__':
    PA = projectApp()
    PA.run()
