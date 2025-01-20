from check_serial_ports import list_serial_ports

PORT = list_serial_ports()
print(PORT)
BAUD_RATE = 115200
RPI_IP_ADDRESS = "http://127.0.0.1:8000"