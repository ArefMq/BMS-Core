#!/usr/bin/env python
import socket
import sys
import array
import sqlite3

from board_model import BoardModel


DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = False


class Receiver:
    def __init__(self, host='', port=2222):
        self.host = host    # Symbolic name meaning all available interfaces
        self.port = port    # Arbitrary non-privileged port
        self.board_model = BoardModel()

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
            print('Data base connected.')
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
        self.board_model.load_from_byte_array(data)

        rows = self.db_connection.execute('SELECT id,channel,pos,status FROM backend_accessories WHERE isAnalog=0')
        db_state = [row[3] for row in rows]

        changed_keys = self.board_model.get_changed_keys()
        if changed_keys:
            for key_id, _ in changed_keys:
                if key_id >= len(db_state):
                    break
                self.set_key_on_db(key_id, 1 - db_state[key_id])
            self.db_connection.commit()
        
    
    def set_key_on_db(self, ith, value):
        print('toggeling %d to %d' % (ith, value))
        self.db_connection.execute('UPDATE backend_accessories SET status=%d WHERE id=%d' % (value, ith + 1))


if __name__ == "__main__":
    receiver = Receiver()

    if DEBUG:
        excepted = KeyboardInterrupt
    else:
        excepted = Exception
        
    try:
        while 1:
            receiver.cycle()
    except excepted:
        pass
    finally:
        receiver.destruct()
