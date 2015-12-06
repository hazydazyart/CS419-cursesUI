import psycopg2
import sys


con = None

con = con = connectt("dbname='postgres' user='postgres'")
cur = con.cursor()
cur.execute("CREATE DATABASE movies")
cur.commit()
con.close()

try:
     
    con = psycopg2.connect("dbname='movies' user='postgres'")
    
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS action")
    cur.execute("DROP TABLE IF EXISTS zombie")
    cur.execute("CREATE TABLE action(Id INTEGER PRIMARY KEY, Name VARCHAR(40), Year INT)")
    cur.execute("INSERT INTO action VALUES(1,'Die Hard',1988)")
    cur.execute("INSERT INTO action VALUES(2,'Terminator 2',1991)")
    cur.execute("INSERT INTO action VALUES(3,'Raiders of the Lost Ark',1981)")
    cur.execute("INSERT INTO action VALUES(4,'Casino Royale',2006)")
    cur.execute("INSERT INTO action VALUES(5,'The Avengers',2012)")
    cur.execute("INSERT INTO action VALUES(6,'Taken', 2008)")
    cur.execute("INSERT INTO action VALUES(7,'Aliens',1986)")
    cur.execute("INSERT INTO action VALUES(8,'Star Wars',1977)")
	
    cur.execute("CREATE TABLE zombie(Id INTEGER PRIMARY KEY, Name VARCHAR(40), Year INT)")
    cur.execute("INSERT INTO zombie VALUES(1,'Dawn of the Dead',1978)")
    cur.execute("INSERT INTO zombie VALUES(2,'Night of the Living Dead',1968)")
    cur.execute("INSERT INTO zombie VALUES(3,'28 Days Later',2002)")
    cur.execute("INSERT INTO zombie VALUES(4,'Shaun of the Dead',2004)")
    cur.execute("INSERT INTO zombie VALUES(5,'Day of the Dead',1985)")
    cur.execute("INSERT INTO zombie VALUES(6,'Dead Snow', 2009)")
    cur.execute("INSERT INTO zombie VALUES(7,'Resident Evil',2002)")
    cur.execute("INSERT INTO zombie VALUES(8,'White Zombie',1932)")
	
    con.commit()
    

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
