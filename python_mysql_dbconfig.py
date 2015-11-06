from configparser import ConfigParser

def read_db_config(filename = 'config.ini', section = 'mysql'):
	"""Read the database configuration file and return a dictionary object
	:param filename: name of configuration file
	:param section: section of the database configuration
	:return: a dictionary of database parameters
	"""
	parser = ConfigParser()
	parser.read(filename)

	db = {}
	if parser.has_section(section):
		items = parser.items(section)
		for item in items:
			db[item[0]] = item[1]
	else:
		raise Exception('{0} not found in the {1} file'.format(section, filename))

	return db
