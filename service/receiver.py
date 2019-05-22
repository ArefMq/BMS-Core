#!/usr/bin/env python
import socket
import sys
import array
import sqlite3


DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False


class Receiver:
    def __init__(self, host='', port=2222):
        self.host = host    # Symbolic name meaning all available interfaces
        self.port = port    # Arbitrary non-privileged port
        self.current_state = None

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')

        except socket.error as exp :
            print('Failed to create socket. Because: %s', str(exp))
            raise

        # Bind socket to local host and port
        try:
            self.socket.bind((self.host, self.port))
            print('Socket bind complete.')

        except socket.error as exp:
            print('Failed to bind the socket. Because: %s', str(exp))
            raise
            
        try:
            self.db_connection = sqlite3.connect(DB_PATH)
            self.db_connection_cursor = self.db_connection.cursor()
        except Exception as exp:
            print('Failed to connect to the database. Because: %s', str(exp))
            raise

    
    def destruct(self):
        self.socket.close()
        self.db_connection.close()

    def cycle(self):
        data, addr = self.socket.recvfrom(1024)

        if not data: 
            raise Exception('invalid data recieved.')
        
        data = bytearray(data.strip())

        if self.current_state is None:
            self.current_state = [data[i] for i in range(14)]
        
        rows = self.db_connection.execute('SELECT id,channel,pos,status FROM backend_accessories')
        db_state = [row[3] for row in rows]

        state_changed = False
        for i in range(14):
            if self.current_state[i] != data[i]:
                self.toggle_key_on_db(i, db_state)
                self.current_state[i] = data[i]
                state_changed = True

            if DEBUG:
                print(data[i])

        if state_changed:
            self.db_connection.commit()

        if DEBUG:
            print('________________________________')
        
    
    def toggle_key_on_db(self, ith, db_state):
        print('toggeling %d' % ith)
        self.db_connection.execute('UPDATE backend_accessories SET status=%d WHERE id=%d' % ((1 - db_state[ith]), ith + 1))


if __name__ == "__main__":
    receiver = Receiver()

    # noinspection PyBroadException
    try:
        while 1:
            receiver.cycle()
    except Exception:
        pass
    finally:
        receiver.destruct()
