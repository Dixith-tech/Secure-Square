from collections import defaultdict
import time

scan_tracker = defaultdict(list)

def detect_port_scan(ip, port):
    current_time = time.time()

    scan_tracker[ip].append((port, current_time))

    recent_ports = [
        p for p, t in scan_tracker[ip]
        if current_time - t < 10
    ]

    if len(set(recent_ports)) > 20:
        return True

    return False