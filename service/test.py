import sqlite3
conn = sqlite3.connect('/home/pi/bms/db.sqlite3')
c = conn.cursor()

# Insert a row of data
for row in c.execute("SELECT id,channel,pos,command FROM backend_status"):
    print row[3] is None

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

