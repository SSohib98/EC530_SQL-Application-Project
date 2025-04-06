import pandas as pd
import sqlite3
import os

LOG_FILE = "error_log.txt"

def log_error(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

def get_existing_schema(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def handle_conflict_strategy(table_name):
    print(f"Table '{table_name}' already exists.")
    choice = input("Choose action - [O]verwrite, [R]ename, [S]kip: ").lower()
    return choice

def create_table_with_conflict_handling(csv_file, table_name):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect("example.db")

    existing_schema = get_existing_schema(conn, table_name)
    if existing_schema:
        choice = handle_conflict_strategy(table_name)
        if choice == 'o':
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        elif choice == 'r':
            new_name = table_name + "_new"
            df.to_sql(new_name, conn, if_exists='replace', index=False)
        elif choice == 's':
            print("Skipped.")
        else:
            msg = f"Invalid choice for table {table_name}"
            print(msg)
            log_error(msg)
    else:
        df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()

create_table_with_conflict_handling("Example.csv", "example_table")
