import npyscreen
import curses
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
    	self.addForm('MYSQL', Mysqlf)
    	self.addForm('POSTGRESQL', Postgref)
    	self.addForm('USERINFO', UserInfo)
    	self.addForm('ADDDB', AddDB)
    	self.addForm('SQLQRY', SQLQuery)
    	self.addForm('VIEWTB', BrowseTable)
    	self.addForm('EDITDB', EditDB)
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
			
		except psycopg2.DatabaseError, e:
			npyscreen.notify_confirm('Could not connect to database. Please try again.')
			return
		
		self.parentApp.switchForm('MAINOPT')
		
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

	def on_ok(self):
		self.parentApp.switchForm('MAIN')

#Show signed in user's information
class Mysqlf(npyscreen.Form):
	
	def create(self):
		msg1 = "Sign into an existing PostgreSQL database or create a new account."
		msg2 = "*Required for non-local databases"
		self.add(npyscreen.TitleFixedText, name = msg1)
		self.add(npyscreen.TitleText, name = "Username:")
		self.add(npyscreen.TitleText, name = "Password:")
		self.add(npyscreen.TitleText, name = "* Host:")
		self.add(npyscreen.TitleText, name = "* Port:")
		self.add(npyscreen.TitleFixedText, name = msg2)
	
	def afterEditing(self):
		self.parentApp.switchForm('MAINOPT')
		
#Main Screen + Menu
class MainOpt(npyscreen.FormBaseNewWithMenus):

	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Select an option from the menu below." )
		self.menu = self.add_menu(name="Main Menu", shortcut="^M")
		self.menu.addItem(text="User Information", onSelect=self.showinfo)
		self.menu.addItem(text="Add PostgreSQL Database", onSelect=self.addDB)
		self.menu.addItem(text="View PostgreSQL Databases", onSelect=self.listDB)
		self.menu.addItem(text="Enter a Query", onSelect=self.SQLQuery)
		self.menu.addItem(text="Browse Table", onSelect=self.BrowseTable)
		self.menu.addItem(text="Create & Modify Databases", onSelect=self.modDB)
		self.menu.addItem(text="Query Databases", onSelect=self.queryDB)
		self.menu.addItem(text="Import a Database", onSelect=self.exDB)
		self.menu.addItem(text="Export a Database", onSelect=self.impDB)
		self.menu.addItem(text="FAQ", onSelect=self.showFAQ)
		self.menu.addItem(text="Exit", onSelect=self.exit)
	
	def showinfo(self):
		self.parentApp.switchForm('USERINFO')
	
	def addDB(self):
		self.parentApp.switchForm('ADDDB')
		
	def listDB(self):
		self.parentApp.switchForm('LISTDB')
	
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

#Show signed in user's information
class UserInfo(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Name:", value="John Johnson")
		self.add(npyscreen.TitleFixedText, name = "Role:", value="User")
		self.add(npyscreen.TitleFixedText, name = "Number of Databases", value="2")
	
	def afterEditing(self):
		self.parentApp.switchFormPrevious()

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
class FAQ(npyscreen.Form):
	
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Show FAQs here")
		
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
#Create PostgreSQL database
class AddDB(npyscreen.Form):
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
		msg = createDB(name, owner)
		npyscreen.notify_confirm(msg)
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
		self.query = self.add(npyscreen.MultiLineEdit,
			value="""Enter query here!""", max_height=5, rely=9)
	
	def afterEditing(self):
		msg = executeQuery(self.query.value)
		npyscreen.notify_confirm(msg)
		self.parentApp.switchFormPrevious()
		
#Get all values from table
class BrowseTable(npyscreen.Form):
	def create(self):
		self.add(npyscreen.TitleFixedText, name="Browse Table")
		grid = self.add(npyscreen.GridColTitles)
		data = selectAll('zombie')
		grid.values = data
	def afterEditing(self):
		self.parentApp.switchFormPrevious()
		
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

def createDB(dbname, owner):
	con = None
	msg = 'Successfully created database ' + dbname
	try:
		con = psycopg2.connect(dbname="postgres", user="postgres")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		command = "CREATE DATABASE " + dbname + " WITH OWNER " + owner
		cur.execute(command)
		rows = cur.fetchall()
	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		msg = 'Error creating database, ' + e
	finally:
		if con:
			con.close()
		return msg
		
def selectAll(table):
	con = None
	output = []
	try:
		con = psycopg2.connect(dbname="movies", user="postgres")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		cur.execute("SELECT * FROM zombie")
		output.append(cols)
		values = cur.fetchall()
		for row in values:
			output.append(row)
	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		print "Error fetching data"
	finally:
		if con:
				con.close()
		return output
		
def executeQuery(query):
	global psqlCon
	msg = 'Successfully executed query!'
	try:
		psqlCon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = psqlCon.cursor()
		cur.execute(query)
	except psycopg2.DatabaseError, e:
		if psqlCon:
			psqlCon.rollback()
		msg = 'Error: ' + e
	finally:
		return msg
	
if __name__ == '__main__':
    PA = projectApp()
    PA.run()
