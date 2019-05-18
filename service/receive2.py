'''
	Simple udp socket server
'''

import socket
import sys
import array
import sqlite3

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 2222	# Arbitrary non-privileged port

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

def reverse_mask(x):
    x = ((x & 0x55555555) << 1) | ((x & 0xAAAAAAAA) >> 1)
    x = ((x & 0x33333333) << 2) | ((x & 0xCCCCCCCC) >> 2)
    x = ((x & 0x0F0F0F0F) << 4) | ((x & 0xF0F0F0F0) >> 4)
    x = ((x & 0x00FF00FF) << 8) | ((x & 0xFF00FF00) >> 8)
    x = ((x & 0x0000FFFF) << 16) | ((x & 0xFFFF0000) >> 16)
    return x

def main():
	#now keep talking with the client
	while 1:
		# receive data from client (data, addr)
                print 'before'
		d = s.recvfrom(1024)
                print 'after'
		data = d[0]
		addr = d[1]

		if not data: 
			break
		
		reply = 'OK...' + data
		
		# s.sendto(b , ('127.0.0.1',2223))
		# print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + bytearray(data.strip())
		a = bytearray(data.strip())
		# for i in range(1, 7):
		# 	qq = format(a[i], '08b')[::-1]
		# 	for j in range(0,7):
		# 		c.execute('SELECT * FROM backend_status WHERE channel=? AND pos=?', (i, j)
		# 		print c.fetchone()
		# 		print '-------------------'



		print '________________________________'
		print a[0]
		print a[1]
		print a[2]
		print a[3]
		print a[4]
		print a[5]
		print a[6]
		print a[7]
		print a[8]
		print a[9]
		print a[10]
		print a[11]
		print a[12]
		print a[13]

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		s.close()
