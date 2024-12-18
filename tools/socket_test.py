import numpy as np
import socket
import threading
import traceback
import copy
import time
import os
import signal

# Switch to using device as socket server instead of reverse socket

cognex_host = '192.168.1.175'  # IP address of cognex device
cognex_port = 3000
c = socket.create_connection((cognex_host, cognex_port))

while True:
    string_data = c.recv(1024).decode("utf-8")
    print(string_data)
