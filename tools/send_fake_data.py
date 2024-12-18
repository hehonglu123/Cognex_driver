import socket
import time

dat = "{;bracket:-34.627,21.423,3.680,98.395,;light:-338.172,-69.265,4.782,99.324\r\n"

# Switch to using a socket server to send data

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('localhost', 3000))
ss.listen(1)
ss.settimeout(1)

while True:
    try:
        s, addr = ss.accept()
    except socket.timeout:
        continue

    with s:
        while True:
            try:
                s.send(dat.encode("ascii"))
                time.sleep(0.5)
            except Exception as e:
                print(f"Error: {e}")
                if isinstance(e, KeyboardInterrupt):
                    raise
                break
