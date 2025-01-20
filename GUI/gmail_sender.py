import smtplib
from email.mime.text import MIMEText
from datetime import datetime

import random
import string

def generate_transaction_id():
    # Generate a random alphanumeric string of length 6
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))



def send_email(subject, body, recipients):
    password = "cqct klpf ehro hbnj"
    sender = "info.sfaclibrary@gmail.com"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def borrow_email(name, receiver, book_title, transaction_id):
    subject = f"SFAC - Library Borrowed Book Notification ({transaction_id})"
    body = f'''
Good day {name}!

You have received this transaction notification from our system. Here are some details:

Transaction ID: {transaction_id}
Borrowed Book Timestamp: {str(datetime.now())}
Borrowed Book Title: {book_title}

Please take note of the following:
1. Books must be returned within one day.
2. Keep books in good condition; damages may incur penalties.
3. A late fee of 5 PHP applies for overdue books.
4. Borrowers are responsible for replacement or repair costs.

Thank you for using the RFID bookshelf system to enhance your library experience!

BEYOND THE BASICS LIBRARY!

SFAC RFID Library
    '''

    send_email(subject, body, [receiver,])

def return_email(name, receiver, book_title, transaction_id):
    subject = f"SFAC - Library Returned Book Notification ({transaction_id})"
    body = f'''
Good day {name}!

You have received this transaction notification from our system. Here are some details:

Transaction ID: {transaction_id}
Returned Book Timestamp: {str(datetime.now())}
Returned Book Title: {book_title}

Thank you for using the RFID bookshelf system to enhance your library experience!

BEYOND THE BASICS LIBRARY!

SFAC RFID Library
    '''

    send_email(subject, body, [receiver,])

if __name__ == "__main__":
    
    name = "Anthony Aldrin Beltran"
    receiver = "anthonyaldrin.beltran@gmail.com"
    book_title = "Romeo and Juliet"
    

    # borrow_email(name,receiver, book_title,transaction_id=generate_transaction_id())
    return_email(name,receiver, book_title,transaction_id=generate_transaction_id())