
import os
import platform
import getpass
import socket

def collect_system_info():
    info = {
        "Operating System": platform.system(),
        "Kernel Version": platform.release(),
        "System Architecture": platform.machine(),
        "Hostname": socket.gethostname(),
        "Current Username": getpass.getuser(),
        "User ID": os.getuid(),
        "Group ID": os.getgid()
    }
    return info

def display_system_info(info):
    print("\n===== SYSTEM INFORMATION =====")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    system_info = collect_system_info()
    display_system_info(system_info)

