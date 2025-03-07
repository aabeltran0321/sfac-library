# Define all RFID commands
RFID_cmdnub = {
    0: [0xBB, 0x00, 0x03, 0x00, 0x01, 0x00, 0x04, 0x7E],  # 0. Hardware version
    1: [0xBB, 0x00, 0x03, 0x00, 0x01, 0x01, 0x05, 0x7E],  # 1. Software version
    2: [0xBB, 0x00, 0x03, 0x00, 0x01, 0x02, 0x06, 0x7E],  # 2. Manufacturers
    3: [0xBB, 0x00, 0x22, 0x00, 0x00, 0x22, 0x7E],        # 3. Single polling instruction
    4: [0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E],  # 4. Multiple polling instructions
    5: [0xBB, 0x00, 0x28, 0x00, 0x00, 0x28, 0x7E],        # 5. Stop multiple polling instructions
    6: [0xBB, 0x00, 0x0C, 0x00, 0x13, 0x01, 0x00, 0x00, 0x00, 0x20,
        0x60, 0x00, 0x30, 0x75, 0x1F, 0xEB, 0x70, 0x5C, 0x59, 0x04,
        0xE3, 0xD5, 0x0D, 0x70, 0xAD, 0x7E],              # 6. Set the SELECT parameter instruction
    7: [0xBB, 0x00, 0x0B, 0x00, 0x00, 0x0B, 0x7E],        # 7. Get the SELECT parameter
    8: [0xBB, 0x00, 0x12, 0x00, 0x01, 0x01, 0x14, 0x7E],  # 8. Set the SELECT mode
    9: [0xBB, 0x00, 0x39, 0x00, 0x09, 0x00, 0x00, 0x00, 0x00, 0x03,
        0x00, 0x00, 0x00, 0x08, 0x4D, 0x7E],              # 9. Read label data storage area
    10: [0xBB, 0x00, 0x49, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x03,
         0x00, 0x00, 0x00, 0x04, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x71, 0x7E],  # 10. Write label data
    11: [0xBB, 0x00, 0x82, 0x00, 0x07, 0x00, 0x00, 0xFF, 0xFF, 0x02, 0x00, 0x80, 0x09, 0x7E],  # 11. Lock label data
    12: [0xBB, 0x00, 0x65, 0x00, 0x04, 0x00, 0x00, 0xFF, 0xFF, 0x67, 0x7E],  # 12. Inactivate kill tag
    13: [0xBB, 0x00, 0x11, 0x00, 0x02, 0x00, 0xC0, 0xD3, 0x7E],  # 13. Set communication baud rate
    14: [0xBB, 0x00, 0x0D, 0x00, 0x00, 0x0D, 0x7E],        # 14. Get Query command parameters
    15: [0xBB, 0x00, 0x0E, 0x00, 0x02, 0x10, 0x20, 0x40, 0x7E],  # 15. Set Query parameters
    16: [0xBB, 0x00, 0x07, 0x00, 0x01, 0x01, 0x09, 0x7E],  # 16. Set up work area
    17: [0xBB, 0x00, 0x08, 0x00, 0x00, 0x08, 0x7E],        # 17. Acquire work locations
    18: [0xBB, 0x00, 0xAB, 0x00, 0x01, 0x01, 0xAC, 0x7E],  # 18. Set up working channel
    19: [0xBB, 0x00, 0xAA, 0x00, 0x00, 0xAA, 0x7E],        # 19. Get the working channel
    20: [0xBB, 0x00, 0xAD, 0x00, 0x01, 0xFF, 0xAD, 0x7E],  # 20. Auto frequency hopping
    21: [0xBB, 0x00, 0xB0, 0x00, 0x00, 0xB0, 0x7E],        # 21. Set RF power
    22: [0xBB, 0x00, 0xB1, 0x00, 0x00, 0xB1, 0x7E],        # 22. Get RF power
    23: [0xBB, 0x00, 0xB6, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x01, 0xB6, 0x7E],  # 23. Frequency hopping setting
    24: [0xBB, 0x00, 0xB5, 0x00, 0x00, 0xB5, 0x7E],        # 24. Frequency hopping state acquisition
    25: [0xBB, 0x00, 0xB2, 0x00, 0x02, 0x00, 0x10, 0xC4, 0x7E],  # 25. Set frequency
    26: [0xBB, 0x00, 0xB3, 0x00, 0x00, 0xB3, 0x7E],        # 26. Get frequency
    27: [0xBB, 0x00, 0xB4, 0x00, 0x01, 0x01, 0xB6, 0x7E],  # 27. Set tag demodulation parameters
    28: [0xBB, 0x00, 0xB7, 0x00, 0x00, 0xB7, 0x7E],        # 28. Get tag demodulation parameters
    29: [0xBB, 0x00, 0x70, 0x00, 0x02, 0x03, 0x03, 0x78, 0x7E],  # 29. Set tag masking area
    30: [0xBB, 0x00, 0x71, 0x00, 0x00, 0x71, 0x7E],        # 30. Get tag masking area
    31: [0xBB, 0x00, 0xA1, 0x00, 0x01, 0x00, 0xA2, 0x7E],  # 31. Save tag configuration parameters
    32: [0xBB, 0x00, 0xA2, 0x00, 0x00, 0xA2, 0x7E],        # 32. Load tag configuration parameters
    33: [0xBB, 0x00, 0x77, 0x00, 0x00, 0x77, 0x7E],        # 33. Reset device
    34: [0xBB, 0x00, 0x75, 0x00, 0x00, 0x75, 0x7E],        # 34. Set device address
    35: [0xBB, 0x00, 0x76, 0x00, 0x00, 0x76, 0x7E],        # 35. Get device address
    36: [0xBB, 0x00, 0x64, 0x00, 0x01, 0x01, 0x66, 0x7E],  # 36. Set heartbeat packet switch
    37: [0xBB, 0x00, 0x62, 0x00, 0x00, 0x62, 0x7E],        # 37. Get heartbeat packet status
    38: [0xBB, 0x00, 0x7A, 0x00, 0x00, 0x7A, 0x7E],        # 38. Factory reset
}

def bytes_to_list(byte_data, format="hex"):
    """
    Convert a bytes object to a list of integers in hexadecimal or decimal format.

    Parameters:
    - byte_data (bytes): The input bytes object.
    - format (str): "hex" for hexadecimal output, "dec" for decimal output. Default is "hex".

    Returns:
    - list: A list of integers in the specified format.
    """
    if format == "hex":
        return [f"{byte:02X}" for byte in byte_data]
    elif format == "dec":
        return [byte for byte in byte_data]
    else:
        raise ValueError("Invalid format. Use 'hex' or 'dec'.")

# Example for sending Command 3 and 9 using Serial
import serial
import time

# Set up serial communication
ser = serial.Serial('COM22', 115200, timeout=1)  # Update with the correct port
time.sleep(2)  # Give some time for the connection to stabilize

# Function to send a command
def send_command(command):
    ser.write(bytearray(command))
    time.sleep(0.5)  # Wait for a response
    response = ser.read(ser.in_waiting)  # Read all available data
    return bytes_to_list(response)

# Send Command 3 (Single polling instruction)
response_3 = send_command(RFID_cmdnub[4])
#print("Response for Command 3:", response_3)

# Send Command 9 (Read label data storage area)
response_9 = send_command(RFID_cmdnub[9])
#print("Response for Command 9:", response_9)

drawer = []
data = response_3
for i,dd in enumerate(data):
    if dd == 'BB' and data[i+1] == '02':
        rfid_code = data[i+8:(i+22)]
        #sent = f"{rfid_code[6]}{rfid_code[7]}{rfid_code[8]}{rfid_code[19]}{rfid_code[20]}{rfid_code[21]}".upper()
        sent = "".join(rfid_code)
        #print(sent)
        if sent not in drawer:
            drawer.append(sent)
            print(drawer)
# Close the serial port
ser.close()
