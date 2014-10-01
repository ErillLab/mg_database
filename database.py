import sqlite3

# Header: create_database
# This function initializes a sqlite database with the name equal to the passed in parameter
# Input: name - The name of the database. ex "test.db" 
# Output: cur - a cursor that will allow the user to execute sql statements.
def create_database(name):
	conn = sqlite3.connect(name)
	return conn

#The promoter is the score and sequence

# Header: create_tables
# This function initializes the tables and view within the our database
# input: a connection that is linked to the newly created database
# output: Tables are created within the database.
def create_tables(conn):
	cur = conn.cursor()
	cur.execute('''CREATE TABLE operon (Sequence text)''')
	cur.execute('''CREATE TABLE gene (Location text, TaxID int, COGID int, RefGeneID int, RefGeneEvalue real, OperonID int, Operon_Pos int)''')
	cur.execute('''CREATE TABLE operon_gene_map (GeneID int, Operon_ID, int)''')
	cur.execute('''CREATE TABLE taxonomy (Domain text, Kingdom text, Phylum text, Class text, 'Order' text, Family text, Genus text, Species text)''')
	cur.execute('''CREATE TABLE cog (Name text, CategoryID int)''')
	cur.execute('''CREATE TABLE category (Category text)''')
	cur.execute('''CREATE TABLE cog_gene_map (GeneID int, COG_ID, int)''')
	cur.execute('''CREATE TABLE processing_parameters(Start int, End int, Evalue real, Sequence text, Intergenic_Distance int)''')
	cur.execute('''CREATE VIEW taxonomy_gene AS SELECT TaxID, COG, OperonID, Domain, Kingdom, Phylum, Class, 'Order', Family, Genus, Species FROM (gene join taxonomy) WHERE gene.TaxID=taxonomy.ROWID''')


# Header: insert_into_table
# This function initializes the tables and view within the our database
# input: a connection that is linked with the database,
#		 the name of the table to insert data,
#		 The values to be inserted into the table 
#		ex. connection, "gene", ("Test", 1, 1, 1)
# output: Tables are created within the database.
def insert_into_table(conn, table, values):
	cur  = conn.cursor()
	statement = "INSERT INTO %s " % table
	statement += "VALUES (" + ",".join('"' + item + '"' for item in values) + ")"
	cur.execute(statement)

# Header: close_connection
# This function is suppose to commit all changes to the sqlite database and then close the connection
# input: A connection that is linked to a database
# Output: finialized changes to the database and the connection is closed.
def close_connection(conn):
	conn.commit()
	conn.close()

# Header: select_from_table
# This function well grab either everything or specified fields from a particular table
# input: a connection that is linked to a database, the table name, the fields you want (array type), and special conditions
# ex. connection, "gene", "*", "Taxonomy = 1"
# ex2. connection, "gene", "*"
# Output: a list containing all of the found search.
def select_from_table(conn, table,fields, conditions=None):
	cur = conn.cursor()
	statement = "SELECT * FROM %s" % table
	if len(fields) > 1:
		statement = "SELECT %s FROM %s" % (",".join(fields), table)
	if conditions  != None:
		statement += " WHERE %s" % conditions
	cur.execute(statement)
	return cur.fetchall()

