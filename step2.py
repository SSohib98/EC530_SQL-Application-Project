import pandas as pd
import sqlite3

def infer_dtype(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    else:
        return "TEXT"

def create_table_from_csv(csv_file, table_name):
    df = pd.read_csv(csv_file)
    columns = ", ".join([f"{col} {infer_dtype(dtype)}" for col, dtype in zip(df.columns, df.dtypes)])
    
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

create_table_from_csv("Example.csv", "example_table_dynamic")
