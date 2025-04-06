import pandas as pd
import sqlite3

# Load CSV into DataFrame
df = pd.read_csv("Example.csv")

# Connect to SQLite
conn = sqlite3.connect("example.db")
cursor = conn.cursor()

# Create table manually
cursor.execute("""
CREATE TABLE IF NOT EXISTS example_table (
    column1 TEXT,
    column2 INTEGER,
    column3 REAL
);
""")

# Insert DataFrame into table
df.to_sql("example_table", conn, if_exists='replace', index=False)

# Run a basic query
cursor.execute("SELECT * FROM example_table LIMIT 5;")
print(cursor.fetchall())

conn.close()
