from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
from Parser_WTA import Parser
from threading import Thread
from serialport import HardwareSerial
import os
from werkzeug.utils import secure_filename

PORT = "COM12"
BAUD_RATE = 115200

app = Flask(__name__)
extension = "./"
SFAC_DATABASE = f'{extension}sfac_library.db'

rfid_code = ""

UPLOAD_FOLDER = 'static/sfac_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/sfac/Dashboard')
def sfac_home():

    conn = sqlite3.connect(SFAC_DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    user_rows = cursor.fetchall()
    cursor.execute('SELECT * FROM Books')
    book_rows = cursor.fetchall()
    conn.close()
    data = {
        'total_books': len(book_rows),
        'total_members': len(user_rows),
        'total_penalty': 0,
        'total_borrowed': 0,
        'total_returned': 0,
        'total_not_returned': 0
    }
    return render_template('sfac_Dashboard.html', **data)
'''
#BOOKS 
# 
#
# 
'''
@app.route('/sfac/Books')
def sfac_books():
    try:
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
        
        return render_template('sfac_Books.html', book_data=book_data)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
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


'''
#Students 
# 
#
# 
'''
@app.route('/sfac/Students')
def sfac_students():
    try:
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

        # Render the template with the fetched data
        return render_template('sfac_Students.html', table_data=table_data)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/sfac/Transaction')
def sfac_transaction():
    borrow_data = [
        {
            'id_no': '1001',
            'name': 'Alice Johnson',
            'book_id': 'B001',
            'book_title': 'The Great Gatsby',
            'borrow_date': '2024-01-01',
            'return_date': '2024-01-15',
            'status': 'Returned'
        },
        {
            'id_no': '1002',
            'name': 'Bob Smith',
            'book_id': 'B002',
            'book_title': 'To Kill a Mockingbird',
            'borrow_date': '2024-01-05',
            'return_date': '2024-01-20',
            'status': 'Not Returned'
        },
        {
            'id_no': '1003',
            'name': 'Charlie Brown',
            'book_id': 'B003',
            'book_title': '1984',
            'borrow_date': '2024-01-10',
            'return_date': '2024-01-25',
            'status': 'Returned'
        }
    ]
    return render_template('sfac_Transaction.html', borrow_data=borrow_data)
# Helper function to connect to the database
def sfac_get_db_connection():
    conn = sqlite3.connect(SFAC_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/sfac/rfid_code_empty', methods=['POST'])
def sfac_rfid_code_empty():
    global rfid_code
    try:
        rfid_code = ""
        return jsonify({'message': 'Remove RFID successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sfac/get_rfid_code')
def sfac_get_rfid_code():
    enroll_rfid = Parser("Enroll ","\r",1,200)
    Serial1 = HardwareSerial(PORT)
    try:
        Serial1.begin(BAUD_RATE)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    while True:
        while Serial1.available():
            c = Serial1.read()
            c = c.decode()

            if enroll_rfid.available(c):
                rfid_code = enroll_rfid.data.replace(" ", "")
                print(rfid_code)
                Serial1.close()
                return jsonify({'message': rfid_code}), 200
            
@app.route('/sfac/get_uhf_rfid_code')
def sfac_get_uhf_rfid_code():
    rfid_parser1 = Parser('uhf', '\r', 1, 500)
    Serial1 = HardwareSerial(PORT)
    try:
        Serial1.begin(BAUD_RATE)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    while True:
        if Serial1.available():
            c = Serial1.read()
            c = c.decode()
            if rfid_parser1.available(c):
                dat = rfid_parser1.data.split("-")
                rfid_drawer_no = dat[0]
                data = dat[1].split("7e")
                for cd in data:
                    rfid_code = cd.split(" ")
                    if(cd.startswith("bb 02 22 00 11") and len(rfid_code)>20):
                        
                        #print(len(rfid_code), rfid_code)
                        rssi =int(rfid_code[5], 16)
                        rfid_code = f"{rfid_code[6]}{rfid_code[7]}{rfid_code[8]}{rfid_code[19]}{rfid_code[20]}{rfid_code[21]}".upper()
                        print(rssi, rfid_code)
                        Serial1.close()
                        return jsonify({'message': rfid_code}), 200
    
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
        ''', (id_number, last_name, first_name, middle_name, email, rfid))
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


def loop_serial():
    global rfid_code;
    try:
        enroll_rfid = Parser("Enroll ","\r",1,200)
        Serial1 = HardwareSerial(PORT)
        Serial1.begin(BAUD_RATE)
        while True:
            while Serial1.available():
                c = Serial1.read()
                c = c.decode()

                if enroll_rfid.available(c):
                    rfid_code = enroll_rfid.data
                    print(rfid_code)
    except:
        pass

    Serial1.close()

if __name__ == '__main__':
    Thread1 = Thread(target=loop_serial, daemon=True)
    app.run(debug=True)
