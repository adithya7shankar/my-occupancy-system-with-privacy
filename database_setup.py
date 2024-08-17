import sqlite3

conn = sqlite3.connect('building_occupancy.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS occupancy (
    id INTEGER PRIMARY KEY,
    signature BLOB,
    entry_time TEXT,
    exit_time TEXT
)
''')
conn.commit()
conn.close()