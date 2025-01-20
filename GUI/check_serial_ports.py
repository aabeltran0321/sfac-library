import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        return port.device
    return None

if __name__ == "__main__":
    print(list_serial_ports())
