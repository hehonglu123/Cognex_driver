import numpy as np
import socket
import threading
import traceback
import copy
import time
import os
import signal


host = '0.0.0.0'  # IP address of PC, align with Server Host Name in Insight TCP/IP Communication
port = 3000
s = socket.socket()
s.bind((host, port))
s.listen(5)
c, addr = s.accept()

while True:
    string_data = c.recv(1024).decode("utf-8")
    print(string_data)
