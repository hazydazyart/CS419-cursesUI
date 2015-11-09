import npyscreen
import curses

#Main form manager
class projectApp(npyscreen.NPSAppManaged):
    def onStart(self):
    	self.addForm('MAINOPT', MainOpt) 
    	self.mainOptions = MainOpt()
    	self.addForm('MAIN', MainLogin, name="Project UI")
    	self.addForm('USERINFO', UserInfo)
    	self.addForm('ADDDB', AddDB)
    	self.addForm('LISTDB', ListDB)
    	self.addForm('SQLQRY', SQLQuery)
    	self.addForm('VIEWTB', BrowseTable)
    	self.addForm('EDITDB', EditDB)
    	self.addForm('QRYDB', QryDB)
    	self.addForm('IMPORTDB', ImportDB)
    	self.addForm('EXPORTDB', ExportDB)
    	self.addForm('FAQ', FAQ)

#Login Screen
class MainLogin (npyscreen.Form):
		
	def create(self):
		self.add(npyscreen.TitleFixedText, name = "Sign in or create a new account")
		self.un = self.add(npyscreen.TitleText, name="Username")
		self.pw = self.add(npyscreen.TitleText, name="Password")
		self.ch = self.add(npyscreen.TitleSelectOne, max_height=4, value=[1,], name="Select",
			values = ["Sign in", "Create New Account"], scroll_exit=True)
		
		#Sign in or create a new account
		
		#If return true go to main form
		#If return false reload this page with blank values
		
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
	con = None
	msg = 'Successfully executed query!'
	try:
		con = psycopg2.connect(dbname="movies", user="postgres")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		cur.execute(query)
	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		msg = 'Error: ' + e
	finally:
		if con:
				con.close()
		return msg
	
if __name__ == '__main__':
    PA = projectApp()
    PA.run()