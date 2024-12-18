import socket


def _recv_until(s, delim):
    msg = b''
    while True:
        c = s.recv(1024)
        print(c)
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
