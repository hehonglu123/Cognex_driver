import socket


def _recv_until(s, delim):
    msg = b''
    while True:
        c = s.recv(1024)
        if len(c) == 0:
            break
        msg += c
        if len(msg) < len(delim):
            continue
        if msg[-len(delim):] == delim:
            return msg


def _recv_line(s):
    r = b''
    while True:
        c = s.recv(1)
        if c == b'\n':
            return r
        r += c


def _exec_command(s, cmd, exect_return=False):
    s.send(cmd.encode('utf-8') + b'\r\n')
    res1 = int(_recv_line(s))
    if res1 != 1:
        raise Exception(f"Command {cmd} failed: {res1}")
    if exect_return:
        return _recv_line(s)
    return None


def _native_connect(host, passwd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, 23))
        _recv_until(s, b'User: ')
        s.send(b'admin\r\n')
        _recv_until(s, b'Password: ')
        if passwd is not None and passwd != '':
            s.send(passwd.encode('utf-8') + b'\r\n')
        else:
            s.send(b'\r\n')
        _recv_until(s, b'User Logged In\r\n')
        return s
    except:
        try:
            s.close()
        except:
            pass
        raise


def native_exec_command(host, passwd, cmd, expect_return=False):
    s = _native_connect(host, passwd)
    try:
        return _exec_command(s, cmd, expect_return)
    finally:
        s.close()


def native_read_image(host, passwd):
    s = _native_connect(host, passwd)
    try:
        s.send(b'RB\r\n')
        res1 = int(_recv_line(s))
        if res1 != 1:
            raise Exception(f"Command RB failed: {res1}")
        expected_bytes = int(_recv_line(s))
        lines = expected_bytes // 80
        extra_bytes = expected_bytes % 80
        read_bytes = lines * 82
        if extra_bytes > 0:
            read_bytes += extra_bytes + 2
        bmp_hex_data = b''
        while len(bmp_hex_data) < read_bytes:
            r = s.recv(read_bytes - len(bmp_hex_data))
            if len(r) == 0:
                raise Exception("Connection closed")
            bmp_hex_data += r
        checksum = _recv_line(s)
        bmp_bytes = bytes.fromhex(bmp_hex_data.decode('ASCII'))

        return bmp_bytes
    finally:
        s.close()
