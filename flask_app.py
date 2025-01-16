from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
from Parser_WTA import Parser
from threading import Thread
from serialport import HardwareSerial
import os
from werkzeug.utils import secure_filename
import requests
from config import *

Serial1 = HardwareSerial(PORT)

app = Flask(__name__)
extension = "./"


rfid_code = ""




@app.route('/sfac/dashboard')
def sfac_home():
    url = f"{RPI_IP_ADDRESS}/sfac/getnumdata"
    resp = requests.get(url)

    data = resp.json()
    
    return render_template('sfac_Dashboard.html', **data, rpi = RPI_IP_ADDRESS)
'''
#BOOKS 
# 
#
# 
'''
@app.route('/sfac/books')
def sfac_books():
    global Serial1
    try:
        url = f"{RPI_IP_ADDRESS}/sfac/getbooks"
        resp = requests.get(url)

        book_data = resp.json()
        try:
            Serial1.close()
        except:
            pass
        return render_template('sfac_Books.html', book_data=book_data, rpi = RPI_IP_ADDRESS)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    



'''
#Students 
# 
#
# 
'''
@app.route('/sfac/students')
def sfac_students():
    global Serial1
    try:
        url = f"{RPI_IP_ADDRESS}/sfac/getnumstudents"
        resp = requests.get(url)

        table_data = resp.json()
        try:
            Serial1.close()
        except:
            pass
        # Render the template with the fetched data
        return render_template('sfac_Students.html', table_data=table_data, rpi = RPI_IP_ADDRESS)
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/sfac/transaction')
def sfac_transaction():
    global Serial1
    #/sfac/gettransactions
    url = f"{RPI_IP_ADDRESS}/sfac/gettransactions"
    resp = requests.get(url)

    borrow_data = resp.json()
    try:
        Serial1.close()
    except:
        pass
    return render_template('sfac_Transaction.html', borrow_data=borrow_data, rpi = RPI_IP_ADDRESS)


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
    global Serial1
    enroll_rfid = Parser("Enroll ","\r",1,200)
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
    global Serial1
    rfid_parser1 = Parser('uhf', '\r', 1, 500)
    # Serial1 = HardwareSerial(PORT)
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
