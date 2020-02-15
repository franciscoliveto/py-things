import sqlite3

database = "test.db"
conn = sqlite3.connect(database)
c = conn.cursor()

# Create table
c.execute("CREATE TABLE IF NOT EXISTS endpoints \
    (eui TEXT PRIMARY KEY NOT NULL, \
    register_type INT NOT NULL, \
    address INT NOT NULL, \
    quantity INT NOT NULL, \
    status TEXT NOT NULL)")

# Insert a row of data
#c.execute("INSERT INTO endpoints VALUES ('1212',0,0,6,'offline')")
eui = '1212'
t = ('offline', eui)
c.execute("UPDATE endpoints SET status=? WHERE eui=?", t)

# Save (commit) the changes
conn.commit()

# We can also close the cursor if we are done with it
c.close()
conn.close()
