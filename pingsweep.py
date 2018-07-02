#!/usr/bin/python3
### Written by revolverdrummer ###
### June 2018 ###
### This script only applies to /24 networks as it stands. Edit the first three octets to scan different networks ###
import os
import sys
import socket

def get_ip():
	#IP Solution from Jamieson Becker, Stack Overflow.
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# doesn't even have to be reachable
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP


#Initializing variables
count = 1
lines = []
ips = []

#Extract first three octets.
local = get_ip()
local = local.split('.')
local = '.'.join(local[0:3])
local = local+"."

#Loop through all /24 available address space
while count <= 254:
	strcount = str(count)
	ip = local+strcount
	#Sends one packet, waits 1/3 of a second for reply. Outputs to a file to avoid cluttering the terminal with ping info.
	command = "ping "+ip+" -c 1 -i 0.3 -q > commandDump.tmp"
	if count != 254:
		#Creates percentage counter with escape character as \r instead of \n.
		percentage = count * .39
		strpercentage = str(round(percentage, 1))
		print (strpercentage+"% Done", end='\r')
	else:
		#Rounds final answer to 100%
		percentage = 100
		strpercentage = str(percentage)
		print (strpercentage+"% Done", end='\r')
	#Evaluates return value on command to determine if address is up (0 means yes).
	up = True if os.system(command) is 0 else False
	count=count+1
	if up == True:
		#Adds IP to list of active hosts if it is not alreadt in that list (shouldn't be).
		if ip not in ips:
			ips.append(ip)
#Cleans tmp dump file
os.system("rm commandDump.tmp")
#Makes list of IPs into string of IPs
ips = str(ips)
with open('addresses.log', 'w') as log:
	log.write(ips)
print ("The IPs that were active are: "+ips+".\n You can find these results in addresses.log")
input("Press [Enter] to close")
