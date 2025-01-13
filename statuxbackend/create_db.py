import sqlite3

def create_database():
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()

    # Create the internships table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT NOT NULL
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and internships table created successfully.")

if __name__ == "__main__":
    create_database()