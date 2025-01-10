import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('sfac_library.db')
cursor = conn.cursor()

# Create Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id_number TEXT PRIMARY KEY,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    rfid TEXT NOT NULL UNIQUE
);
''')

# Create Books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    rfid_code TEXT PRIMARY KEY,
    book_id TEXT NOT NULL UNIQUE,
    book_title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    publisher TEXT NOT NULL
);
''')

# Create BorrowedBooks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS BorrowedBooks (
    id_no TEXT NOT NULL,
    name TEXT NOT NULL,
    book_id TEXT NOT NULL,
    book_title TEXT NOT NULL,
    borrow_date TEXT NOT NULL,
    return_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (id_no) REFERENCES Users (id_number),
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables created successfully!")
