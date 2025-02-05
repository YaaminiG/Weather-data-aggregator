import sqlite3

# Connect to the SQLite database (replace 'weather_data.db' with your actual database file)
conn = sqlite3.connect('weather_data.db')

# Create a cursor object
cursor = conn.cursor()

# Retrieve all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in the database:", tables)

# Query data from a specific table (replace 'weather' with your table name)
cursor.execute("SELECT * FROM weather;")
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
