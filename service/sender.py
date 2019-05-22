#!/usr/bin/env python
import socket
import sys
import array
import sqlite3
from time import sleep
from board_model import BoardModel

DB_PATH = '/home/pi/BMS-Core/bms/db.sqlite3'
DEBUG = True
SENDING_DELAY = 1.1


class Sender:
    def __init__(self, host='192.168.1.1', port=2223):
        self.HOST = host # Symbolic name meaning all available interfaces
        self.PORT = port # Arbitrary non-privileged port
        self.board_model = BoardModel()

        # Datagram (udp) socket
        try :
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('Socket created')
        except socket.error as exp:
            print('Failed to create socket. Because: %s', str(exp))
            raise


        # Bind socket to local host and port
        try:
            self.socket.bind(('', self.PORT))
            print('Socket bind complete')
        except socket.error as exp:
            print('Failed to bind the socket. Because: %s', str(exp))
            raise
    

        try:
            self.db_connection = sqlite3.connect(DB_PATH)
            self.db_cursor_connection = self.db_connection.cursor()
            print('Data base connected.')
        except Exception as exp:
            print('Failed to connect to the database. Because: %s', str(exp))
            raise

    def destruct(self):
        self.socket.close()
        self.db_connection.close()
    
    def get_from_db(self):
        res = self.db_connection.execute("SELECT id,channel,pos,status FROM backend_accessories")
        byte_data = [row[3] for x in res]
        return byte_data
        
    def send(self):
        byte_data = self.get_from_db()

        for key, state in self.board_model.get_changed_keys():
            print('change state of %d to %d' % (key, state))

        if DEBUG:
            print('sending: ', [r for r in self.board_model.to_byte_array()])
        res = self.socket.sendto(self.board_model.to_byte_array() , (self.HOST, self.PORT))
        if res and DEBUG:
            print('send-to function fail: %d' % res)


if __name__ == "__main__":
    sender = Sender()
    
    try:
        while 1:
            sender.send()
            sleep(SENDING_DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        sender.destruct()
