import socket
import time

dat = "{;bracket:-34.627,21.423,3.680,98.395,;light:-338.172,-69.265,4.782,99.324\r\n"

s = socket.create_connection(('localhost', 3000))

while True:
    s.send(dat.encode("ascii"))
    time.sleep(0.5)
