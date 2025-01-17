import socket
import requests
import ipaddress

def get_default_gateway():
    """
    Get the default gateway IP address using socket.
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    subnet = local_ip.rsplit('.', 1)[0]  # Extract the subnet (e.g., 192.168.1)
    return subnet

def find_server_on_network(port=8000):
    """
    Scan the gateway subnet from 1-255 and find the active server.
    """
    gateway_subnet = get_default_gateway()
    for i in range(1, 256):
        ip = f"{gateway_subnet}.{i}"
        url = f"http://{ip}:{port}"
        try:
            response = requests.get(url, timeout=0.5)
            if response.status_code == 200:
                print(f"Server found at {url}")
                return url  # Return the correct IP and port
        except requests.exceptions.RequestException:
            pass  # Ignore unreachable IPs
    print("No server found in the network range.")
    return None

if __name__ == "__main__":
    server_url = find_server_on_network(port=8000)
    if server_url:
        print(f"Correct Server URL: {server_url}")
    else:
        print("No accessible server detected.")
