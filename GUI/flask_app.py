
from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
from flask_cors import CORS
from Parser_WTA import Parser
from serialport import HardwareSerial
from check_serial_ports import list_serial_ports
import time
import hashlib
import json
from gmail_sender import generate_transaction_id, borrow_email, return_email
from datetime import datetime
from process_rfid import borrow_rfid, return_rfid

app = Flask(__name__)
CORS(app)

PORT = list_serial_ports()
Serial1 = HardwareSerial(PORT)
extension = "./"
SFAC_DATABASE = f'{extension}sfac_library.db'
if PORT is None:
    print("No Serial Port Detected!")
    exit()
print(PORT)

UPLOAD_FOLDER = 'static/sfac_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def dict_to_hash(data: dict) -> str:
    return json.dumps(data, sort_keys=True)

def hash_to_dict(data_string) -> dict:
    return json.loads(data_string)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to connect to the database
def sfac_get_db_connection():
    conn = sqlite3.connect(SFAC_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/')
def index():
    return "SFAC-LIBRARY"

@app.route('/sfac/getnumdata')
def getnumdata():
    conn = sqlite3.connect(SFAC_DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    user_rows = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    book_rows = cursor.fetchall()
    cursor.execute("SELECT * FROM BorrowedBooks where status = 'borrowed'")
    borrowed_books = cursor.fetchall()
    cursor.execute("SELECT * FROM BorrowedBooks where status = 'returned'")
    returned_books = cursor.fetchall()
    conn.close()
    data = {
        'total_books': len(book_rows),
        'total_members': len(user_rows),
        'total_penalty': 0,
        'total_borrowed': len(borrowed_books),
        'total_returned': len(returned_books),
        'total_not_returned': 0
    }
    return jsonify(data)

@app.route('/sfac/getnumstudents')
def getnumstudents():
    # Connect to the database
    conn = sqlite3.connect(SFAC_DATABASE)
    conn.row_factory = sqlite3.Row  # Enable row-based access to data
    cursor = conn.cursor()

    # Query to select data from the Users table with full name concatenated
    cursor.execute('''
        SELECT id_number, 
                last_name || " " || first_name || " " || middle_name AS full_name,
                first_name, 
                middle_name,
                last_name, 
                email, 
                rfid 
        FROM Users
    ''')
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    table_data = [dict(row) for row in rows]

    # Close the database connection
    conn.close()
    return jsonify(table_data)
@app.route('/sfac/gettransactions', methods=['GET'])
def gettransactions():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(SFAC_DATABASE)
        cursor = conn.cursor()
        
        # Fetch all data from BorrowedBooks table
        cursor.execute("""
            SELECT transaction_id, id_no, name, book_id, book_title, borrow_date, return_date, status
            FROM BorrowedBooks
        """)
        rows = cursor.fetchall()
        
        # Convert data into a list of dictionaries
        borrow_data = [
            {
                'transaction_id': row[0],
                'id_no': row[1],
                'name': row[2],
                'book_id': row[3],
                'book_title': row[4],
                'borrow_date': row[5],
                'return_date': row[6] if row[6] else '-',
                'status': row[7].capitalize()
            }
            for row in rows
        ]
        print(borrow_data)
        # Close the connection
        conn.close()
        
        return jsonify(borrow_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sfac/getbooks')
def getbooks():
    conn = sqlite3.connect(SFAC_DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    rows = cursor.fetchall()
    
    # Prepare data to be sent to the template
    book_data = []
    for row in rows:
        book_data.append({
            'rfid_code': row[0],  # Assuming rfid_code is the first column in the Books table
            'book_id': row[1],     # Assuming book_id is the second column
            'book_title': row[2],  # Assuming book_title is the third column
            'author': row[3],      # Assuming author is the fourth column
            'genre': row[4],       # Assuming genre is the fifth column
            'publisher': row[5],    # Assuming publisher is the sixth column
            'book_path': row[6]
        })
    conn.close()
    return jsonify(book_data)

# Route to insert data into Users table
@app.route('/sfac/add-user', methods=['POST'])
def sfac_add_user():
    data = request.json  # Get JSON data from the request
    try:
        # Extract fields from the request
        id_number = data.get('id_number')
        last_name = data.get('last_name')
        first_name = data.get('first_name')
        middle_name = data.get('middle_name')
        email = data.get('email')
        rfid = data.get('rfid')

        # Validate required fields
        if not all([id_number, last_name, first_name, middle_name, email, rfid]):
            return jsonify({'error': 'All fields are required'}), 400

        # Insert data into the database
        conn = sfac_get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Users (id_number, last_name, first_name, middle_name, email, rfid)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (id_number, last_name.capitalize(), first_name.capitalize(), middle_name.capitalize(), email, rfid))
        conn.commit()
        conn.close()

        return jsonify({'message': 'User added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sfac/update_user', methods=['POST'])
def sfac_update_user():
    try:
        # Get the user data from the request
        user_data = request.get_json()

        # Extract individual fields
        id_number = user_data['id_number']
        last_name = user_data['last_name']
        first_name = user_data['first_name']
        middle_name = user_data['middle_name']
        email = user_data['email']
        rfid = user_data['rfid']

        # Connect to the database
        conn = sqlite3.connect(SFAC_DATABASE)
        cursor = conn.cursor()

        # Update the user in the database
        cursor.execute('''
            UPDATE Users
            SET last_name = ?, first_name = ?, middle_name = ?, email = ?, rfid = ?
            WHERE id_number = ?
        ''', (last_name, first_name, middle_name, email, rfid, id_number))

        # Commit the changes
        conn.commit()

        # Close the database connection
        conn.close()

        # Return a success response
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/sfac/delete_user', methods=['DELETE'])
def sfac_delete_user():
    try:
        # Get the user ID from the request
        user_data = request.get_json()
        id_number = user_data['id_number']

        # Connect to the database
        conn = sqlite3.connect(SFAC_DATABASE)
        cursor = conn.cursor()

        # Delete the user from the database
        cursor.execute('''
            DELETE FROM Users WHERE id_number = ?
        ''', (id_number,))

        # Commit the changes
        conn.commit()

        # Close the database connection
        conn.close()

        # Return a success response
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# Route to insert data into BorrowedBooks table
@app.route('/sfac/add-borrowed-book', methods=['POST'])
def sfac_add_borrowed_book():
    data = request.json  # Get JSON data from the request
    try:
        # Extract fields from the request
        id_no = data.get('id_no')
        name = data.get('name')
        book_id = data.get('book_id')
        book_title = data.get('book_title')
        borrow_date = data.get('borrow_date')
        return_date = data.get('return_date')
        status = data.get('status')

        # Validate required fields
        if not all([id_no, name, book_id, book_title, borrow_date, return_date, status]):
            return jsonify({'error': 'All fields are required'}), 400

        # Insert data into the database
        conn = sfac_get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO BorrowedBooks (id_no, name, book_id, book_title, borrow_date, return_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id_no, name, book_id, book_title, borrow_date, return_date, status))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Borrowed book record added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/sfac/addBook', methods=['POST'])
def sfac_add_book():
    try:
        # Retrieve form data
        rfid_code = request.form['rfid_code']
        book_id = request.form['book_id']
        book_title = request.form['book_title']
        author = request.form['author']
        genre = request.form['genre']
        publisher = request.form['publisher']

        # Handle photo upload
        if 'book_photo' not in request.files:
            return jsonify({'status': 'error', 'message': 'No photo uploaded'}), 400

        file = request.files['book_photo']
        if file and allowed_file(file.filename):
            filename = f"{book_id}{file.filename[-4:]}"
            print(file.filename)
            photo_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
            file.save(photo_path)
        else:
            photo_path = None

        # Insert data into the Books table
        conn = sqlite3.connect(SFAC_DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Books (rfid_code, book_id, book_title, author, genre, publisher, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (rfid_code, book_id, book_title, author, genre, publisher, photo_path))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Book added successfully'}), 201
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/sfac/delete_book', methods=['DELETE'])
def sfac_delete_book():
    try:
        book_data = request.get_json()
        book_id = book_data['book_id']

        conn = sqlite3.connect(SFAC_DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))

        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500






# Home route
@app.route('/welcome')
def welcome():
    global Serial1

    try:
        Serial1.close()
    except:
        pass
    return render_template('welcome.html')

@app.route('/transaction')
def transaction():
    user_id = request.args.get('user_id', '')  # Get the 'user_input' query parameter
    user = get_user_by_rfid(user_id)
    try:
        conn = sfac_get_db_connection()
        cursor = conn.cursor()

        # Query the database
        query = "SELECT * FROM BorrowedBooks WHERE id_no = ?"
        cursor.execute(query, (user["id_number"],))
        rows = cursor.fetchall()
        transaction_data = [
            {
                'transaction_id': row[0],
                'id_no': row[1],
                'name': row[2],
                'book_id': row[3],
                'book_title': row[4],
                'borrow_date': row[5],
                'return_date': row[6] if row[6] else '-',
                'status': row[7].capitalize()
            }
            for row in rows
        ]
        try:
            isBorrowed = transaction_data[-1]["status"] == "Borrowed"
        except:
            isBorrowed = False
        return render_template('transaction.html', user_id = user_id, transaction_data = transaction_data, isBorrowed=isBorrowed)
    except:
        pass
    


@app.route('/selection')
def selection():
    global Serial1
    try:
        Serial1.close()
    except:
        pass
    genre = request.args.get('user_input', '')  # Get the 'user_input' query parameter
    type1 = request.args.get('type', '')            # Get the 'type' query parameter
    user_id = request.args.get('user_id', '')  # Get the 'user_input' query parameter

    conn = sqlite3.connect(SFAC_DATABASE)
    cursor = conn.cursor()

    if genre:  # If a genre is specified, filter by genre
        cursor.execute('''
            SELECT * FROM Books WHERE genre = ?
        ''', (genre.capitalize(),))
    else:  # If no genre is specified, select all books
        cursor.execute('''
            SELECT * FROM Books
        ''')

    books = cursor.fetchall()  # Fetch the filtered or full list of books
    if books:
        conn.close()
        print(books)
        return render_template(
            'selection.html',
            user_input=genre.upper(),
            type1=type1,
            genre=genre,
            books=books,
            user_id=user_id,
            book_title = "",
            photo_path = ""
        )
    else:
        transaction_id = request.args.get('transaction', '')    
        book_title = genre
        cursor.execute('''
        SELECT genre, photo_path FROM Books where book_title = ?
            ''', (book_title,))
        data = cursor.fetchone()
        print(data)
        cursor.execute('''
            SELECT * FROM Books WHERE genre = ?
        ''', (data[0].capitalize(),))
        books = cursor.fetchall()
        return render_template(
            'selection.html',
            user_input=genre.upper(),
            type1=type1,
            genre=data[0].upper(),
            books=books,
            user_id=user_id,
            book_title = book_title,
            photo_path = data[1],
            transaction_id = transaction_id
        )
         
        
@app.route('/category')
def category():
    user_input = request.args.get('user_input', None)  # Get the 'user_input' query parameter
    user_id = request.args.get('user_id', '')  # Get the 'user_input' query parameter
    return render_template('category.html',user_input=user_input, user_id = user_id)

# Form route
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return render_template('form_response.html', name=name, message=message)
    return render_template('form.html')

@app.route('/sfac/get_rfid_code')
def sfac_get_rfid_code():
    global Serial1
    enroll_rfid = Parser("PROCESS ","\r",1,200)
    try:
        Serial1.begin(115200)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    while True:
        while Serial1.available():
            c = Serial1.read()
            c = c.decode()

            if enroll_rfid.available(c):
                rfid_code = enroll_rfid.data.replace(" ", "")
                print(rfid_code)
                user = get_user_by_rfid(rfid_code)
                print(user)
                if len(user.keys())>1:
                    Serial1.close()
                    jsonify({"message": rfid_code})
    
@app.route('/get_books_by_photo_path', methods=['POST'])
def get_books_by_photo_path():
    # Parse JSON request
    data = request.get_json()
    photo_path = data.get('photo_path')
    type1 = data.get('type')
    rfid_code = data.get('user_id')

    # Validate inputs
    if not photo_path  or not rfid_code:
        return jsonify({"error": "Missing required fields: photo_path, type, or user_id."}), 400

    try:
        # Open database connection
        conn = sfac_get_db_connection()
        cursor = conn.cursor()

        # Query the database
        query = "SELECT * FROM Books WHERE photo_path = ?"
        cursor.execute(query, (photo_path,))
        book = cursor.fetchone()

        # Close connection
        
        #print(hash_to_dict(user_id))
        if book:
            global Serial1
            try:
                Serial1.close()
            except:
                pass
            book_rfid_code = book["rfid_code"]
            book_genre = book["genre"]
            user = get_user_by_rfid(rfid_code)
            name = f"{user['last_name'].capitalize()}, {user['first_name'].capitalize()} {user['middle_name'].capitalize()}"
            
            print(book_rfid_code, book_genre, type1)

            if type1.lower() == "borrow":
                transaction_id = generate_transaction_id()
                
                json_file_path = "rfid_codes_by_genre.json"
                borrow_rfid(json_file_path, book_rfid_code, book_genre, PORT)
                borrow_book(transaction_id, user['id_number'], name, book["book_id"], book["book_title"])
                borrow_email(name, user["email"], book["book_title"], transaction_id)
            else:
                transaction_id = data.get('transaction_id')
                json_file_path = "rfid_codes_by_genre.json"
                return_rfid(json_file_path, book_rfid_code, book_genre, PORT)
                print(transaction_id)
                return_book(transaction_id)
                return_email(name, user["email"], book["book_title"], transaction_id)

                
            

            conn.close()
            return jsonify({"message": "Done"})
        else:
            return jsonify({"message": "No book found with the specified path."}), 404

    except sqlite3.Error as e:
        return jsonify({"error": "Database error: " + str(e)}), 500               

def get_user_by_rfid(rfid):
    # Establish database connection
    conn = sfac_get_db_connection()
    cursor = conn.cursor()
    
    # Execute query to select user by RFID
    cursor.execute('''
        SELECT id_number, last_name, first_name, middle_name, email, rfid
        FROM Users
        WHERE rfid = ?
    ''', (rfid,))
    
    # Fetch the result
    user = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # If user is found, return JSON; else return a message
    if user:
        user_data = {
            "id_number": user[0],
            "last_name": user[1],
            "first_name": user[2],
            "middle_name": user[3],
            "email": user[4],
            "rfid": user[5]
        }
        return user_data
    else:
        return {"message": "User not found"}


# Insert data when borrowing a book
def borrow_book(transaction_id, id_no, name, book_id, book_title):
    conn = sfac_get_db_connection()
    cursor = conn.cursor()
    borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
    return_date = ""  # Leave return date blank for borrowing
    status = "borrowed"
    
    # Insert data into BorrowedBooks table
    cursor.execute("""
        INSERT INTO BorrowedBooks (transaction_id, id_no, name, book_id, book_title, borrow_date, return_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (transaction_id, id_no, name, book_id, book_title, borrow_date, return_date, status))
    conn.commit()
    print("Book borrowed successfully!")

# Update data when returning a book
def return_book(transaction_id):
    conn = sfac_get_db_connection()
    cursor = conn.cursor()
    return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time for returning
    status = "returned"
    
    # Check if the transaction exists
    cursor.execute("""
        SELECT * FROM BorrowedBooks WHERE transaction_id = ? AND status = 'borrowed'
    """, (transaction_id,))
    record = cursor.fetchone()
    
    if record:
        # Update the record with return date and status
        cursor.execute("""
            UPDATE BorrowedBooks
            SET return_date = ?, status = ?
            WHERE transaction_id = ? AND status = 'borrowed'
        """, (return_date, status, transaction_id))
        conn.commit()
        print("Book returned successfully!")
    else:
        print("No borrowed book found for the given transaction ID.")
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
