import socket
import threading

open_ports_with_banner = []
open_ports_no_banner = []
def grab_banner(s):
    try:
        banner = s.recv(1024).decode().strip()
        return banner
    except:
        return ""

def scan_port(target, port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        s.connect((target, port))
        banner = grab_banner(s)
        if banner:
            open_ports_with_banner.append(port)
        else:
            open_ports_no_banner.append(port)
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()

def banner_grabbing_port_scan(target, port_range):
    threads = []
    total_objects = max(range(*port_range))
    five_percent = total_objects * 0.05
    last_open_ports = 0
    for port in range(*port_range):
        t = threading.Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()
        # Print progress every 5%
        index = len(threads)
        if index % int(five_percent) == 0:
            progress = (index / total_objects) * 100
            open_ports = len(open_ports_with_banner) + len(open_ports_no_banner)
            print(f"\rProgress: {progress:.2f}%, open ports: {open_ports}  ", end='', flush=True)

    for t in threads:
        t.join()

# Example usage:
target_ip = '192.168.1.130'  # Replace with your target IP
ports = (1, 65535)
banner_grabbing_port_scan(target_ip, ports)
print("\r")
print(f"Open Ports on: {target_ip}, without Banner: {str(open_ports_no_banner)}")
print(f"Open Ports on: {target_ip},    with Banner: {str(open_ports_with_banner)}")
