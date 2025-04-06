import sqlite3

def list_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]

def main():
    conn = sqlite3.connect("example.db")
    print("Welcome to the Spreadsheet Chat CLI!")

    while True:
        user_input = input("\nEnter a command (list/run/exit): ").strip().lower()

        if user_input == "list":
            tables = list_tables(conn)
            print("Tables:", tables)

        elif user_input == "run":
            query = input("Enter SQL query: ")
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                for row in results:
                    print(row)
            except Exception as e:
                print("Error:", e)

        elif user_input == "exit":
            print("Goodbye!")
            break

        else:
            print("Unknown command.")

    conn.close()

if __name__ == "__main__":
    main()
