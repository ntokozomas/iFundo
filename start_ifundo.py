import socket
import subprocess
import sys
import os

import datetime

def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# Create a little startup timestamp for logs
print(f"🕰️ Ifundo booting at {datetime.datetime.now()}")

script_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(script_dir, "venv", "bin", "python")

if is_online():
    print("🌐 Online mode activated")
    subprocess.run([venv_python, os.path.join(script_dir, "ifundo_online.py")])
else:
    print("📴 Offline mode activated")
    subprocess.run([venv_python, os.path.join(script_dir, "ifundo_offline.py")])

