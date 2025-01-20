import json
import time
from serialport import HardwareSerial
import play_error
import play_success
import time
from Parser_WTA import Parser
# Load the initial JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Main loop
def borrow_rfid(json_file, removed_rfid, expected_genre, PORT):
    initial_json = load_json(json_file)
    Serial1 = HardwareSerial(PORT)
    Serial1.begin(115200)

    cabinets = {
        "Romance": 1,
        "Thriller": 2,
        "General": 3,
    }
    while True:
        # Load the JSON file
        try:
            current_data = load_json(json_file)
            Serial1.prints(f"g{cabinets[expected_genre]}?")

            

            if removed_rfid not in current_data[expected_genre]:
                play_success.play()
                print("Success!")
                Serial1.prints("x1?x2?x3?")
                Serial1.close()
                return
            else:
                for k1 in current_data.keys():
                    if len(current_data[k1]) != len(initial_json[k1]):
                        Serial1.prints(f"r{cabinets[k1]}?")
                        play_error.play()
                        Serial1.prints(f"x{cabinets[k1]}?")
        except Exception as e:
            print(e)
        time.sleep(1)
def return_rfid(json_file, returned_rfid, expected_genre, PORT):

    initial_json = load_json(json_file)
    Serial1 = HardwareSerial(PORT)
    Serial1.begin(115200)

    cabinets = {
        "Romance": 1,
        "Thriller": 2,
        "General": 3,
    }
    while True:
        # Load the JSON file
        try:
            current_data = load_json(json_file)
            Serial1.prints(f"g{cabinets[expected_genre]}?")

            if returned_rfid in current_data[expected_genre]:
                play_success.play()
                print("Success!")
                Serial1.prints("x1?x2?x3?")
                return
            else:
                for k1 in current_data.keys():
                    if returned_rfid in current_data[k1]:
                        Serial1.prints(f"r{cabinets[k1]}?")
                        play_error.play()
                        Serial1.prints(f"x{cabinets[k1]}?")

                        
        except Exception as e:
            print(e)
        time.sleep(1)

# Example usage
if __name__ == "__main__":
    from check_serial_ports import list_serial_ports
    # Path to the JSON file
    json_file_path = "rfid_codes_by_genre.json"

    # The RFID code to monitor and its expected genre
    monitored_rfid = "3000E214F30C"       # Example RFID code
    monitored_genre = "General"   # Expected genre for the RFID code

    PORT = list_serial_ports()

    print(PORT)

    # Start monitoring
    # borrow_rfid(json_file_path, monitored_rfid, monitored_genre, PORT)
    # return_rfid(json_file_path, monitored_rfid, monitored_genre, PORT)
    Serial1 = HardwareSerial(PORT)
    rfid_parser1 = Parser('uhf', '\r', 1, 500)
    # Serial1 = HardwareSerial(PORT)
    Serial1.begin(115200)

    drawer3 = []

    while True:
        if Serial1.available():
            c = Serial1.read()
            c = c.decode()
            if rfid_parser1.available(c):
                dat = rfid_parser1.data.split("-")
                rfid_drawer_no = dat[0]
                dd = dat[1].split(" ")
                for i,d in enumerate(dd):
                    if d == 'bb':
                        if dd[i+1]=="02":
                            rfid_code = dd[i:24]
                            if len(rfid_code)>20:
                                if rfid_drawer_no == '3':
                                    sent = "".join(rfid_code[8:-2])
                                    print(sent)
                                    if sent not in drawer3:
                                        drawer3.append(sent)
                                        print(drawer3)
                # data = dat[1].split("7e")
                # for cd in data:
                #     rfid_code = cd.split(" ")
                #     if(cd.startswith("bb 02 22 00 11") and len(rfid_code)>19):
                        
                #         #print(len(rfid_code), rfid_code)

                #         if rfid_drawer_no == '3':
                #             print(len(rfid_code), rfid_code)
                            # rssi =int(rfid_code[5], 16)
                            # rfid_code = f"{rfid_code[6]}{rfid_code[7]}{rfid_code[8]}{rfid_code[19]}{rfid_code[20]}{rfid_code[21]}".upper()
                            # print(rssi, rfid_code, rfid_drawer_no)
                            # if rfid_code not in drawer3:
                            #     drawer3.append(rfid_code)
                            #     print(drawer3)