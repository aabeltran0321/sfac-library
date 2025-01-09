from flask import Flask, render_template

app = Flask(__name__)

@app.route('/sfac/Dashboard')
def home():
    data = {
        'total_books': 1200,
        'total_members': 350,
        'total_penalty': 450,
        'total_borrowed': 800,
        'total_returned': 750,
        'total_not_returned': 50
    }
    return render_template('sfac_Dashboard.html', **data)

@app.route('/sfac/Books')
def books():
    book_data = [
        {
            'rfid_code': 'A12345',
            'book_id': 'B001',
            'book_title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'genre': 'Fiction',
            'publisher': 'Scribner'
        },
        {
            'rfid_code': 'A12346',
            'book_id': 'B002',
            'book_title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'genre': 'Fiction',
            'publisher': 'J.B. Lippincott & Co.'
        },
        {
            'rfid_code': 'A12347',
            'book_id': 'B003',
            'book_title': '1984',
            'author': 'George Orwell',
            'genre': 'Dystopian',
            'publisher': 'Secker & Warburg'
        }
    ]
    return render_template('sfac_Books.html', book_data=book_data)

@app.route('/sfac/Students')
def students():
    table_data = [
        {'id_number': '1001', 'name': 'Alice Johnson', 'email': 'alice@example.com', 'rfid': '123456'},
        {'id_number': '1002', 'name': 'Bob Smith', 'email': 'bob@example.com', 'rfid': '654321'},
        {'id_number': '1003', 'name': 'Charlie Brown', 'email': 'charlie@example.com', 'rfid': '789012'}
    ]
    return render_template('sfac_Students.html', table_data=table_data)

@app.route('/sfac/Transaction')
def transaction():
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

if __name__ == '__main__':
    app.run(debug=True)
