import MySQLdb

db = MySQLdb.connect("localhost","root","zxc@123","cool" )

cursor = db.cursor()

cursor.execute("SELECT VERSION()")

# disconnect from server
db.close()