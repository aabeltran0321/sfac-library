from serialport import HardwareSerial
from Parser_WTA import Parser


rfid_parser1 = Parser('uhf', '\r', 1, 500)
Serial1 = HardwareSerial('COM8')

Serial1.begin(115200)

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
                