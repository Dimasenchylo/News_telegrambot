import MySQLdb
from MySQLdb import cursors
from keys import hostname, username, password, database, database1

HOSTNAME = hostname
USERNAME = username
PASSWORD = password
DATABASE = database
DATABASE1 = database1

conn_mysql = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD)
crsr_mysql = conn_mysql.cursor()

# Create the database if it doesn't exist
query = f"CREATE DATABASE IF NOT EXISTS {DATABASE}"
crsr_mysql.execute(query)
print("Database created successfully")

# Connect to the created database
conn = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE, cursorclass=cursors.DictCursor)
crsr_mysql = conn.cursor()

# Create the "orders" table if it doesn't exist
sql_command = """
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    descr VARCHAR(200),
    url VARCHAR(200)
    );
"""

crsr_mysql.execute(sql_command)

# Create database for premium
connection_mysql = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD)
cursor_mysql = connection_mysql.cursor()

# Create the database if it doesn't exist
query = f"CREATE DATABASE IF NOT EXISTS {DATABASE1}"
cursor_mysql.execute(query)
print("Database1 created successfully")

# Connect to the created database
connection = MySQLdb.connect(host=HOSTNAME, user=USERNAME, passwd=PASSWORD, db=DATABASE1, cursorclass=cursors.DictCursor)
cursor_mysql = connection.cursor()

# Create the "orders" table if it doesn't exist
sql_command = """
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INT(40),
    premium VARCHAR(200)
    );
"""

cursor_mysql.execute(sql_command)