#!/usr/bin/env python
import socket
import sys
import array
import sqlite3


DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False


class Receiver:
    def __init__(self, port=2222):
        self.host = ''    # Symbolic name meaning all available interfaces
        self.port = port    # Arbitrary non-privileged port

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as msg :
            print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            raise

        # Bind socket to local host and port
        try:
            self.socket.bind((self.host, self.port))
            print('Socket bind complete.')
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
            
        self.db_connection = sqlite3.connect(DB_PATH)
        self.db_connection_cursor = self.db_connection.cursor()

        self.current_state = None
    
    def destruct(self):
        self.socket.close()
        self.db_connection.close()

    def recieve(self):
        d = self.socket.recvfrom(1024)
        data = d[0]
        addr = d[1]

        if not data: 
            raise Exception('invalid data recieved.')
        
        a = bytearray(data.strip())

        if self.current_state is None:
            self.current_state = [a[i] for i in range(14)]
        
        rows = self.db_connection.execute('SELECT id,channel,pos,status FROM backend_accessories')
        db_state = [row[3] for row in rows]

        does_toggle_happened = False
        for i in range(14):
            if self.current_state[i] != a[i]:
                self.toggle_key_on_db(i, db_state)
                self.current_state[i] = a[i]
                does_toggle_happened = True

            if DEBUG:
                print(a[i])

        if does_toggle_happened:
            self.db_connection.commit()

        if DEBUG:
            print('________________________________')
        
    
    def toggle_key_on_db(self, ith, db_state):
        print('toggeling %d' % ith)
        self.db_connection.execute('UPDATE backend_accessories SET status=%d WHERE id=%d' % ((1 - db_state[ith]), ith + 1))


if __name__ == "__main__":
    receiver = Receiver()
    
    try:
        while 1:
            receiver.recieve()
    except KeyboardInterrupt:
        pass
    finally:
        receiver.destruct()
