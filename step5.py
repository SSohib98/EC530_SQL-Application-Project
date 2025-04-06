import os
import sqlite3
import pandas as pd
import openai

# Ensure your OpenAI API key is set either in environment or as a direct string
openai.api_key = os.getenv("OPENAI_API_KEY")  # or you can set your key directly here

# Function to load CSV into SQLite
def load_csv_to_sqlite(csv_file, db_file):
    # Read CSV into DataFrame
    df = pd.read_csv(csv_file)

    # Create SQLite connection
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Dynamically create table based on CSV columns
    table_name = os.path.splitext(os.path.basename(csv_file))[0]
    columns = ", ".join([f"{col} TEXT" for col in df.columns])

    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
    cursor.execute(create_table_sql)

    # Insert DataFrame rows into SQLite table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

# Function to inspect schema of the database
def get_schema(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = [col[1] for col in columns]

    conn.close()
    return schema

# Function to interact with AI and generate SQL from user query
def ask_ai_to_generate_sql(user_query, schema):
    prompt = f"""You are an AI assistant tasked with converting user queries into SQL statements.
The database uses SQLite and contains the following tables:
{schema}
User Query: \"{user_query}\"
Your task is to:
1. Generate a SQL query that accurately answers the user's question.
2. Ensure the SQL is compatible with SQLite syntax.
3. Provide a short comment explaining what the query does.

Output Format:
- SQL Query
- Explanation
"""

    response = openai.Completion.create(
        model="gpt-4",  # Use the latest model
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response['choices'][0]['text'].strip()

# Main function to interact with user
def main():
    db_file = 'example.db'  # SQLite database file
    schema = {}
    
    print("AI Spreadsheet Assistant\nType commands like:\n- load example.csv\n- Ask any question about the data\n- exit")

    while True:
        user_input = input("\nDescribe your data question (or type 'exit'): ")

        if user_input.lower() == 'exit':
            print("Exiting program.")
            break
        elif user_input.lower().startswith('load'):
            # Load the CSV file
            csv_file = user_input.split()[1]  # Assuming input is 'load <filename.csv>'
            print(f"Loading {csv_file} into database...")
            load_csv_to_sqlite(csv_file, db_file)
            schema = get_schema(db_file)  # Refresh schema after loading the CSV
            print(f"Schema Loaded:\n{schema}")
        else:
            if not schema:
                print("⚠ Please load a CSV first.")
                continue
            
            # Pass user query and schema to AI for SQL generation
            print("Generating SQL...")
            ai_response = ask_ai_to_generate_sql(user_input, schema)
            print(f"AI Response:\n{ai_response}")

# Run the assistant
if __name__ == "__main__":
    main()
