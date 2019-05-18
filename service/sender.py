#!/usr/bin/env python
import socket
import sys
import array
import sqlite3
from time import sleep


DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = True


class Sender:
    def __init__(self, host='192.168.1.1', port=2223):
        self.HOST = host # Symbolic name meaning all available interfaces
        self.PORT = port # Arbitrary non-privileged port

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error, msg:
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            raise


        # Bind socket to local host and port
        try:
            self.socket.bind(('', self.PORT))
            print('Socket bind complete')
        except socket.error , msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            raise
    

        self.db_connection = sqlite3.connect(DB_PATH)
        self.db_cursor_connection = self.db_connection.cursor()
        print('Data base connected.')

		self.current_state = None

        # FIXME: fix this:
        self.b = bytearray()
        # Mode		
        self.b.append(1)

        # Switches
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)

        # HVAC
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)
        self.b.append(0)

    
    def destruct(self):
        self.socket.close()
        self.db_connection.close()
    
	def update_from_db(self):
		for row in self.db_connection.execute("SELECT id,channel,pos,status FROM backend_accessories"):
            # print '  - ', row[3], row[1], row[2]
            if row[3] == 1:
                self.b[row[1]] = self.b[row[1]] | (1 << row[2])
            else:
                self.b[row[1]] = self.b[row[1]] & ~(1 << row[2])

    def send(self):
		self.update_from_db()

		if self.current_state is None:
            self.current_state = [self.b[i] for i in range(14)]
		
		for i in range(14):
            if self.current_state[i] != self.b[i]:
                print('change state of %d to %d' % (i, self.b[i]))
                self.current_state[i] = self.b[i]
			

        if DEBUG:
            print('sending: ', [r for r in self.b])
        res = self.socket.sendto(self.b , (self.HOST, self.PORT))
        if res:
            print('send-to function fail: %d' % res)


if __name__ == "__main__":
    sender = Sender()
    
    try:
        while 1:
            sender.send()
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        sender.destruct()
        


