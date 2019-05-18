'''
	Simple udp socket server
'''

import socket
import sys
import array
import sqlite3
from time import sleep

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 2223	# Arbitrary non-privileged port

# Datagram (udp) socket
try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()


# Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'
conn = sqlite3.connect('/home/pi/bms/db.sqlite3')
c = conn.cursor()

b = bytearray()
b.append(1)

b.append(0)
b.append(0)
b.append(0)
b.append(0)
b.append(0)
b.append(0)
b.append(0)

b.append(0)
b.append(0)
b.append(0)
b.append(0)
b.append(0)
b.append(0)

#now keep talking with the client

def main():
	while 1:
		for row in c.execute("SELECT id,channel,pos,status FROM backend_accessories"):
			# print '  - ', row[3], row[1], row[2]
			if row[3] == 1:
				b[row[1]] = b[row[1]] | (1 << row[2])
			else:
				b[row[1]] = b[row[1]] & ~(1 << row[2])
		# print "-----------------------------------------"
		# receive data from client (data, addr)
		# msg = raw_input('Enter message to send : ')
		# q = int(msg)
		# w = w ^ (1 << q)
		# print w
		
                print 'sending: ', [r for r in b]
		res = s.sendto(b , ('192.168.1.1',2223))
                print res
		sleep(0.1)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		s.close()
		conn.close()


